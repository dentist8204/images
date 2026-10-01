import json
import re
import subprocess

seccomp_profile = {
  "defaultAction": "SCMP_ACT_ERRNO",
  "defaultErrno": "ENOSYS",
  "architectures": [
    "SCMP_ARCH_X86_64"
  ],
  "syscalls": [
    {
      "action": "SCMP_ACT_ALLOW",
      "names": []
    }
  ]
}

with open("config/seccomp-replacements.json", "r", encoding="utf-8") as replacements_file:
  replacements = json.load(replacements_file)

with open("syscalls.txt", "r", encoding="utf-8") as input_file:
  input = input_file.read()

allowed_ids     = re.findall(r"@\[(\d+)\]", input)
allowed_ids_set = set(allowed_ids)
blocked_ids     = re.findall(r"@error\[(\d+)\]: (\d)", input)
blocked_ids     = [id for id in blocked_ids if id[0] not in allowed_ids_set]

for id in allowed_ids:
  result = subprocess.run(["ausyscall", "x86_64", id], capture_output=True, text=True, check=True)

  name = result.stdout.strip()
  
  if name in replacements:
    seccomp_profile["syscalls"].extend(replacements[name])
  else:
    seccomp_profile["syscalls"][0]["names"].append(name)

seccomp_profile["syscalls"][0]["names"].sort()

for id, errnoRet in blocked_id:
  result = subprocess.run(["ausyscall", "x86_64", id], capture_output=True, text=True, check=True)

  name = result.stdout.strip()
  
  seccomp_profile["syscalls"].append({
    "names": [name],
    "action": "SCMP_ACT_ERRNO",
    "errnoRet": errnoRet,
    "comment": "disallow because it returned the errno while being logged"
  })

with open("seccomp-profile.json", "w", encoding="utf-8") as output_file:
  json.dump(seccomp_profile, output_file, indent=2)
