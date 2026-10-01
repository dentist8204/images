import json
import os
import subprocess
import sys
import time

bpftrace = subprocess.Popen(["sudo", "bpftrace", "-o", "syscalls.txt", "scripts/trace-seccomp-logs.bt"])

bpftrace_exit_code = bpftrace.poll()

if bpftrace_exit_code is not None and bpftrace_exit_code != 0:
  sys.exit(1)

time.sleep(5)

image_name = sys.argv[1]

with open("config/seccomp-tests.json", "r", encoding="utf-8") as seccomp_tests_file:
  seccomp_tests = json.load(seccomp_tests_file)[image_name]

username      = sys.argv[3]
runtime_dir   = sys.argv[4]
container_ids = []

for test in seccomp_tests:
  try:
    create_command = ["sudo", "-u", f"{username}",
                      "env", f"XDG_RUNTIME_DIR={runtime_dir}",
                      "podman", "create", "--runtime=crun", "--cap-drop=all",
                      "--workdir=/home/inner-user/entry",
                      f"--security-opt=seccomp=/home/{username}/config/default-docker-log-seccomp.json",
                      f"--volume=/home/{username}/environments/{image_name}:/home/inner-user",
                      f"{sys.argv[2]}/{image_name}:latest"]
  except subprocess.CalledProcessError as error:
    print(f"PODMAN ERROR: {error.stderr}")
    
    raise
  
  create_command.extend(test)
  
  result = subprocess.run(create_command, capture_output=True, text=True, check=True)

  container_id = result.stdout.strip()

  subprocess.run(["sudo", "-u", f"{username}", "env", f"XDG_RUNTIME_DIR={runtime_dir}",
                  "podman", "start", container_id], check=True)
  subprocess.run(["sudo", "-u", f"{username}", "env", f"XDG_RUNTIME_DIR={runtime_dir}", "timeout", "20s",
                  "podman", "wait", container_id], check=True)

subprocess.run(["sudo", "kill", f"{bpftrace.pid}"], check=True)

time.sleep(5)
