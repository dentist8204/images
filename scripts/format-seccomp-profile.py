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

ids = []

with open("syscalls.txt", "r", encoding="utf-8") as input_file:
  for line in input_file:
    match = re.search(r"^@\[(d+)\]", line)

    if match:
      ids.append(match.group(1))

for id in ids:
  result = subprocess.run(["ausyscall", "x86_64", id], capture_output=True, text=True, check=True)

  name = result.stdout.strip()
  
  if name in replacements:
    seccomp_profile["syscalls"].extend(replacements[name])
  else:
    seccomp_profile["syscalls"][0]["names"].append(name)

with open("seccomp-profile.json", "w", encoding="utf-8") as output_file:
  json.dump(data, output_file, indent=2)
