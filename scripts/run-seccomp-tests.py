import json
import os
import subprocess
import sys
import time

bpftrace = subprocess.Popen(["sudo", "bpftrace", "-o", "syscalls.txt", "scripts/trace-seccomp-logs.bt"])

time.sleep(3)

bpftrace_exit_code = bpftrace.poll()

if bpftrace_exit_code is not None and bpftrace_exit_code != 0:
  sys.exit(1)

image_name = sys.argv[1]

with open("config/seccomp-tests.json", "r", encoding="utf-8") as seccomp_tests_file:
  seccomp_tests = json.load(seccomp_tests_file)[image_name]

username      = sys.argv[3]
user_home     = f"/home/{username}"
runtime_dir   = sys.argv[4]
sudo_command  = ["sudo", "-u", f"{username}",
                 "env", f"XDG_RUNTIME_DIR={runtime_dir}", f"HOME={user_home}",
                 f"XDG_CONFIG_HOME={user_home}/.config", f"XDG_DATA_HOME={user_home}/.local/share",
                 f"XDG_CACHE_HOME={user_home}/.cache"]

for i in range(0, len(seccomp_tests)):
  container_name = f"container_name_{i}"
  
  create_command = ["podman", "create", "--runtime=crun", "--cap-drop=all", "--rm",
                    "--workdir=/home/inner-user/entry", f"--name={container_name}",
                    f"--security-opt=seccomp=/home/{username}/config/default-docker-log-seccomp.json",
                    f"--volume=/home/{username}/environments/{image_name}:/home/inner-user",
                    f"{sys.argv[2]}/{image_name}:latest"]
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
  subprocess.run(logs_command, cwd=f"{user_home}")
  subprocess.run(kill_command, cwd=f"{user_home}")
  subprocess.run(wait_command, cwd=f"{user_home}")

time.sleep(3)

subprocess.run(["sudo", "kill", f"{bpftrace.pid}"], check=True)

time.sleep(3)
