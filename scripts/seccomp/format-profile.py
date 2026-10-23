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

allowed_names = set()
blocked_names = set()

with open("config/seccomp/baseline.json", "r", encoding="utf-8") as baseline_file:
  for category in json.load(baseline_file):
    allowed_names.update(category["names"])

with open("syscalls.txt", "r", encoding="utf-8") as input_file:
  input_ = input_file.read()

with open("config/seccomp/clusters.json", "r", encoding="utf-8") as clusters_file:
  temp            = json.load(clusters_file)
  clusters        = temp["clusters"]
  cluster_mapping = temp["mapping"]

with open("config/seccomp/replacements.json", "r", encoding="utf-8") as replacements_file:
  replacements = json.load(replacements_file)

with open("config/seccomp/allowance.json", "r", encoding="utf-8") as allowance_file:
  allowance  = set(json.load(allowance_file))
  allowance -= set(replacements)

with open("config/seccomp/swaps.json", "r", encoding="utf-8") as swaps_file:
  swaps = json.load(swaps_file)

allowed_ids = set(re.findall(r"@\[(\d+)\]", input_))
syscalls    = seccomp_profile["syscalls"]

for id_ in allowed_ids:
  result = subprocess.run(["ausyscall", "x86_64", id_], capture_output=True, text=True, check=True)
  
  name = result.stdout.strip()

  if name in swaps:
    name = swaps[name]

  if name in cluster_mapping:
    allowed_names.update(clusters[cluster_mapping[name]])
  elif name in replacements:
    for rule in replacements[name]:
      syscalls.append({
        "names": [name],
        "action": "SCMP_ACT_ALLOW",
        "args": rule["args"],
        "comment": rule["comment"]
      })

    blocked_names.add(name)
  elif name not in allowance:
    syscalls.append({
      "names": [name],
      "action": "SCMP_ACT_ERRNO",
      "errnoRet": 1,
      "comment": "disallow to cause failure"
    })

    blocked_names.add(name)
  else:
    allowed_names.add(name)

syscalls[0]["names"] = list(allowed_names)
syscalls[0]["names"].sort()

blocked_ids = re.findall(r"@error\[(\d+)\]: (\d+)", input_)
blocked_ids = [id_ for id_ in blocked_ids if id_[0] not in allowed_ids]

for (id_, errnoRet) in blocked_ids:
  result = subprocess.run(["ausyscall", "x86_64", id_], capture_output=True, text=True, check=True)

  name = result.stdout.strip()

  if name in swaps:
    name = swaps[name]

  blocked_names.add(name)
  
  syscalls.append({
    "names": [name],
    "action": "SCMP_ACT_ERRNO",
    "errnoRet": int(errnoRet),
    "comment": "disallow because it returned this errno while being logged"
  })

all_names = allowed_names | blocked_names

with open("config/seccomp/baseline-replacements.json", "r", encoding="utf-8") as baseline_replacements_file:
  for (name, errnoRet) in json.load(baseline_replacements_file).items():
    if name not in all_names:
        syscalls.append({
          "names": [name],
          "action": "SCMP_ACT_ERRNO",
          "errnoRet": errnoRet,
          "comment": "disallow because it sometimes returns this errno while being logged"
        })

with open("seccomp-profile.json", "w", encoding="utf-8") as output_file:
  json.dump(seccomp_profile, output_file, indent=2)
