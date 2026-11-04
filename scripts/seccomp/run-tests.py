import json
import subprocess
import sys
import time

image_name = sys.argv[1]

with open(f"tests/scenarios/{image_name}.json", "r", encoding="utf-8") as seccomp_tests_file:
  seccomp_tests = json.load(seccomp_tests_file)

with open(f"scripts/seccomp/trace-logs.bt", "r", encoding="utf-8") as trace_file:
  trace_script = trace_file.read()

trace_script += f'''
  tracepoint:sched:sched_process_exit
  /pinned && tgid == pinned_pid && tid == tgid/ {{
  @exit_count++;

  if (@exit_count == {len(seccomp_tests)}) {{
    exit();
  }}

  @pinned = 0;
}}
'''

output_file_name = "syscalls.txt"

bpftrace   = subprocess.Popen(["sudo", "bpftrace", "-e", trace_script, "-o", output_file_name])
start_time = time.time()
timeout    = 20

while True:
  try:
    with open(output_file_name, "r", encoding="utf-8") as output_file:
      if "READY" in output_file.read():
        break
  except FileNotFoundError:
    pass

  if time.time() - start_time > timeout:
    bpftrace.terminate()

    sys.exit(f"bpftrace took more than {timeout} seconds to initialize")

  time.sleep(0.1)

username     = sys.argv[3]
user_home    = f"/home/{username}"
sudo_command = ["sudo", "-u", f"{username}",
                "env", f"XDG_RUNTIME_DIR={sys.argv[4]}", f"HOME={user_home}",
                f"XDG_CONFIG_HOME={user_home}/.config", f"XDG_DATA_HOME={user_home}/.local/share",
                f"XDG_CACHE_HOME={user_home}/.cache"]

if len(sys.argv) > 5:
  identifier = f"@{sys.argv[5]}"
else:
  identifier = ":latest"

for i in range(0, len(seccomp_tests)):
  container_name = f"container_name_{i}"
  
  create_command = ["podman", "create", "--runtime=crun", "--cap-drop=all", "--rm",
                    "--workdir=/mnt/workspace/entry", f"--name={container_name}",
                    "--userns=keep-id:uid=1007,gid=1007",
                    "--env=HOME=/mnt/workspace",
                    f"--security-opt=seccomp=/home/{username}/config/seccomp/default-docker-logged.json",
                    f"--volume=/home/{username}/tests/environments/{image_name}:/mnt/workspace",
                    f"{sys.argv[2]}/{image_name}{identifier}"]
  start_command  = ["podman", "start", container_name]
  logs_command   = ["timeout", "60s",
                    "podman", "logs", "-f", container_name]
  kill_command   = ["podman", "kill", container_name]
  wait_command   = ["podman", "wait", "--condition=removing", container_name]
  
  create_command = sudo_command + create_command
  start_command  = sudo_command + start_command
  logs_command   = sudo_command + logs_command
  kill_command   = sudo_command + kill_command
  wait_command   = sudo_command + wait_command
  
  create_command.extend(seccomp_tests[i])
  
  subprocess.run(create_command, cwd=f"{user_home}", check=True)
  subprocess.run(start_command, cwd=f"{user_home}", check=True)
  subprocess.run(logs_command, cwd=f"{user_home}", stderr=subprocess.DEVNULL)
  subprocess.run(kill_command, cwd=f"{user_home}", stderr=subprocess.DEVNULL)
  subprocess.run(wait_command, cwd=f"{user_home}", stderr=subprocess.DEVNULL)

bpftrace.wait(timeout=timeout)
