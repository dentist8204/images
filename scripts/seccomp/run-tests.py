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
  /@tracked[tid]/ {{
  delete(@tracked[tid]);

  @tracked_count[0]--;

  if (@tracked_count[0] == 0) {{
    @exit_count[0]++;
  }}

  if (@exit_count[0] == {len(seccomp_tests)}) {{
    printf("DONE\\n");
    exit();
  }}
}}
'''

output_file_name = "syscalls.txt"

bpftrace       = subprocess.Popen(["sudo", "bpftrace", "-e", trace_script, "-o", output_file_name])
start_time     = time.time()
timeout        = 20
sleep_duration = 0.1

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

  time.sleep(sleep_duration)

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

create_command =\
sudo_command + ["podman", "create", "--runtime=crun", "--cap-drop=all", "--rm",
                "--workdir=/mnt/workspace/entry", "--userns=keep-id:uid=1007,gid=1007",
                "--env=HOME=/mnt/workspace",
                f"--security-opt=seccomp=/home/{username}/config/seccomp/default-docker-logged.json",
                f"--volume=/home/{username}/tests/environments/{image_name}:/mnt/workspace"]

start_command = sudo_command + ["podman", "start"]
logs_command  = sudo_command + ["timeout", "60s", "podman", "logs", "-f"]
kill_command  = sudo_command + ["podman", "kill"]
wait_command  = sudo_command + ["podman", "wait", "--condition=removing"]

for i in range(0, len(seccomp_tests)):
  container_name = f"container_name_{i}"

  create_command_i = create_command + [f"--name={container_name}", f"{sys.argv[2]}/{image_name}{identifier}"]
  create_command_i.extend(seccomp_tests[i])

  start_command_i = start_command + [container_name]
  logs_command_i  = logs_command  + [container_name]
  kill_command_i  = kill_command  + [container_name]
  wait_command_i  = wait_command  + [container_name]
  
  subprocess.run(create_command_i, cwd=f"{user_home}", check=True)
  subprocess.run(start_command_i, cwd=f"{user_home}", check=True)
  subprocess.run(logs_command_i, cwd=f"{user_home}", stderr=subprocess.DEVNULL)
  subprocess.run(kill_command_i, cwd=f"{user_home}", stderr=subprocess.DEVNULL)
  subprocess.run(wait_command_i, cwd=f"{user_home}", stderr=subprocess.DEVNULL)

start_time = time.time()

while True:
  try:
    with open(output_file_name, "r", encoding="utf-8") as output_file:
      if "DONE" in output_file.read():
        break
  except FileNotFoundError:
    pass

  if time.time() - start_time > timeout:
    bpftrace.terminate()

    sys.exit(f"bpftrace took more than {timeout} seconds to finalize")

  time.sleep(sleep_duration)

bpftrace.wait(timeout=3)
