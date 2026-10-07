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

for i in range(0, len(seccomp_tests)):
  container_name = f"container_name_{i}"
  
  run_command = ["sudo", "-u", f"{username}",
                 "env", f"XDG_RUNTIME_DIR={sys.argv[4]}", f"HOME={user_home}",
                 f"XDG_CONFIG_HOME={user_home}/.config", f"XDG_DATA_HOME={user_home}/.local/share",
                 f"XDG_CACHE_HOME={user_home}/.cache",
                 "podman", "run", "--runtime=crun", "--cap-drop=all", "--rm",
                 "--workdir=/home/inner-user/entry", f"--name={container_name}",
                 "--stop-timeout=60",
                 f"--security-opt=seccomp=/home/{username}/config/default-docker-log-seccomp.json",
                 f"--volume=/home/{username}/environments/{image_name}:/home/inner-user",
                 f"{sys.argv[2]}/{image_name}:latest"]
  
  run_command.extend(seccomp_tests[i])
  
  subprocess.run(run_command, cwd=f"{user_home}", check=True)

time.sleep(3)

subprocess.run(["sudo", "kill", f"{bpftrace.pid}"], check=True)

time.sleep(3)
