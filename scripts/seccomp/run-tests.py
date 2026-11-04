import json
import re
import subprocess
import sys

image_name = sys.argv[1]

with open(f"tests/scenarios/{image_name}.json", "r", encoding="utf-8") as seccomp_tests_file:
  seccomp_tests = json.load(seccomp_tests_file)

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
  stop_command   = ["podman", "stop", "--time=3", container_name]
  wait_command   = ["podman", "wait", "--condition=removing", container_name]
  
  create_command = sudo_command + create_command
  start_command  = sudo_command + start_command
  logs_command   = sudo_command + logs_command
  stop_command   = sudo_command + stop_command
  wait_command   = sudo_command + wait_command
  
  create_command.extend(seccomp_tests[i])
  
  subprocess.run(create_command, cwd=f"{user_home}", check=True)
  subprocess.run(start_command, cwd=f"{user_home}", check=True)
  subprocess.run(logs_command, cwd=f"{user_home}", stderr=subprocess.DEVNULL)
  subprocess.run(stop_command, cwd=f"{user_home}", stderr=subprocess.DEVNULL)
  subprocess.run(wait_command, cwd=f"{user_home}", stderr=subprocess.DEVNULL)

result = subprocess.run("sudo ausearch -m SECCOMP | grep 'code=0x7ffc0000'", check=True, shell=True,
                        capture_output=True)

syscalls = re.findall(r'sig=(\d+).*syscall=(\d+)', result.stdout)

success = set(syscall for (sig, syscall) in syscalls if sig == "0")
failure = dict(syscall: sig for (sig, syscall) in syscalls if sig != "0")

with open("syscalls.txt", "w", encoding="utf-8") as output_file:
  for syscall in success:
    output_file.write(f"@[{syscall}]: 1\n")

  for (syscall, sig) in failure.items():
    output_file.write(f"@error[{syscall}]: {sig}\n")
