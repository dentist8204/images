import json
import subprocess
import sys
import time

bpftrace = subprocess.Popen(["sudo", "bpftrace", "-o", "syscalls.txt", "scripts/trace-seccomp-logs.bt"])

time.sleep(5)

with open("config/seccomp-tests.json", "r", encoding="utf-8") as seccomp_tests_file:
  seccomp_tests = json.load(seccomp_tests_file)[sys.argv[1]]

container_ids = []

for test in seccomp_tests:
  result = subprocess.run(["podman", "create", "--runtime=crun", "--cap-drop=all",
                           "--workdir=/home/inner-user/entry",
                           "--security-opt=seccomp=config/default-docker-log-seccomp.json",
                           f"{sys.argv[2]}/{sys.argv[1]}:latest"].extend(test),
                          capture_output=True, text=True)

  container_id = result.stdout.strip()

  subprocess.run(["podman", "start", container_id])
  subprocess.run(["timeout", "20s", "podman", "wait", container_id])

subprocess.run(["sudo", "kill", f"{bpftrace.pid}"])
