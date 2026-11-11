SETTINGS = {
  "network": { "type": bool, "strict": False },

  "uid": { "type": int, "strict": False, "min": 0 },
  "cpu-period": { "type": int, "strict": False, "min": 0 },
  "cpu-quota": { "type": int, "strict": False, "min": 0 },
  "memory": { "type": int, "strict": False, "min": 0 },
  "disk-bps": { "type": int, "strict": False, "min": 0 },
  "disk-iops": { "type": int, "strict": False, "min": 0 },
  "nofile": { "type": int, "strict": False, "min": 0 },
  "locks": { "type": int, "strict": False, "min": 0 },
  "sigpending": { "type": int, "strict": False, "min": 0 },

  "sandbox-path": { "type": bytes, "strict": False, "pattern": rb"/[^\x00]*" },
  "disk-name": { "type": bytes, "strict": False, "pattern": rb"/dev/[^\x00]*" },
  "mount-parent": { "type": bytes, "strict": False, "pattern": rb"/[^\x00]*" },
  "working-dir": { "type": bytes, "strict": False, "pattern": rb"/[^\x00]*" },

  "volumes": { "type": dict, "strict": False },

  "env": { "type": list, "strict": False }
}

VOLUMES = {
  "read_write": { "type": list, "strict": False },
  "read_only": { "type": list, "strict": False },
  "tmpfs": { "type": list, "strict": False }
}

VOLUME_ENTRY = { "type": bytes, "pattern": rb"[^/][^\x00]*" }

# from https://pubs.opengroup.org/onlinepubs/9799919799/
ENV_ENTRY = { "type": bytes, "pattern": rb"[^\x00=]+=[^\x00]*" }

VERIFY_OUTPUT = { "type": list }

VERIFY_ENTRY = {
  "critical": { "type": dict, "strict": True },
  "optional": { "type": dict, "strict": False }
}

VERIFY_ENTRY_CRITICAL = {
  # https://www.rfc-editor.org/info/rfc3986/
  "type": { "type": bytes, "strict": True, "pattern": rb"[a-zA-Z][a-zA-Z0-9+.-]*://[^\x00\s]+"},

  "identity": { "type": dict, "strict": False },
  "image": { "type": dict, "strict": True }
}

VERIFY_ENTRY_CRITICAL_IMAGE = {
  # https://github.com/opencontainers/image-spec/blob/13cff54902ec9ad6320cbc487a685b66fcd67171/descriptor.md#digests
  "docker-manifest-digest": { "type": bytes, "strict": True, "pattern": rb"[a-z0-9]+([+._-][a-z0-9]+)*:[a-zA-Z0-9=_-]+"}
}

ATTEST_OUTPUT = {
  "payload": { "type": str, "strict": True },
  "payloadType": { "type": str, "strict": False },

  "signatures": { "type": list, "strict": False }
}

ATTEST_PAYLOAD = {
  "_type": { "type": str, "strict": False },
  "predicateType": { "type": str, "strict": False },

  "predicate": { "type": dict, "strict": True},

  "subject": { "type": list, "strict": False }
}

ATTEST_PAYLOAD_PREDICATE = {
  "defaultAction": { "type": bytes, "strict": True, "pattern": rb"SCMP_ACT_ERRNO" },

  "defaultErrno": { "type": str, "strict": True },

  "architectures": { "type": list, "strict": True },
  "syscalls": { "type": list, "strict": True }
}

SYSCALLS_ENTRY = {
  "errnoRet": { "type": int, "strict": False, "min": 0 },

  "action": { "type": bytes, "strict": True, "pattern": rb"(SCMP_ACT_ERRNO|SCMP_ACT_ALLOW)" },

  "names": { "type": list, "strict": True },
  "args": { "type": list, "strict": False }
}

REFERENCE = {
  "registry": { "type": bytes, "strict": True, "pattern": rb"[^\x00\s]+" },
  # https://github.com/opencontainers/image-spec/blob/13cff54902ec9ad6320cbc487a685b66fcd67171/descriptor.md#digests
  "digest": { "type": bytes, "strict": True, "pattern": rb"[a-z0-9]+([+._-][a-z0-9]+)*:[a-zA-Z0-9=_-]+"}
}
