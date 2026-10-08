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

with open("config/seccomp-baseline.json", "r", encoding="utf-8") as baseline_file:
  baseline = json.load(baseline_file)

allowed_names = []

for category in baseline:
  allowed_names.extend(category["names"])

with open("syscalls.txt", "r", encoding="utf-8") as input_file:
  input = input_file.read()

with open("config/seccomp-clusters.json", "r", encoding="utf-8") as clusters_file:
  temp            = json.load(clusters_file)
  clusters        = temp["clusters"]
  cluster_mapping = temp["mapping"]

with open("config/seccomp-replacements.json", "r", encoding="utf-8") as replacements_file:
  replacements = json.load(replacements_file)

with open("config/seccomp-swaps.json", "r", encoding="utf-8") as swaps_file:
  swaps = json.load(swaps_file)

allowed_ids = set(re.findall(r"@\[(\d+)\]", input))
syscalls    = seccomp_profile["syscalls"]

for id in allowed_ids:
  result = subprocess.run(["ausyscall", "x86_64", id], capture_output=True, text=True, check=True)
  
  name = result.stdout.strip()

  if name in cluster_mapping:
    allowed_names.append(name)
    allowed_names.extend(clusters[cluster_mapping[name]])
  elif name in swaps:
    allowed_names.append(swaps[name])
  elif name in replacements:
    syscalls.extend(replacements[name])
    syscalls.append({
      "names": [name],
      "action": "SCMP_ACT_ERRNO",
      "errnoRet": 1,
      "comment": "disallow to cause failure"
    })
  else:
    allowed_names.append(name)

syscalls[0]["names"] = list(allowed_names)
syscalls[0]["names"].sort()

blocked_ids = re.findall(r"@error\[(\d+)\]: (\d)", input)
blocked_ids = [id for id in blocked_ids if id[0] not in allowed_ids]

for id, errnoRet in blocked_ids:
  result = subprocess.run(["ausyscall", "x86_64", id], capture_output=True, text=True, check=True)

  name = result.stdout.strip()
  
  syscalls.append({
    "names": [name],
    "action": "SCMP_ACT_ERRNO",
    "errnoRet": int(errnoRet),
    "comment": "disallow because it returned this errno while being logged"
  })

with open("seccomp-profile.json", "w", encoding="utf-8") as output_file:
  json.dump(seccomp_profile, output_file, indent=2)
