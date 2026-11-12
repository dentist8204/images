__PRINTABLE     = rb"[\x21-\x7e]+"

_ABSOLUTE_PATH    = { "type": bytes, "pattern": rb"/[^\x00]*" }
_PRINTABLE        = { "type": bytes, "pattern": __PRINTABLE }
_PRINTABLE_STRICT = { "type": bytes, "strict": True, "pattern": __PRINTABLE }

# from https://github.com/opencontainers/image-spec/blob/13cff54902ec9ad6320cbc487a685b66fcd67171/descriptor.md#digests
_MANIFEST_DIGEST = { "type": bytes, "strict": True, "pattern": rb"[a-z0-9]+([+._-][a-z0-9]+)*:[a-zA-Z0-9=_-]+" }

_NON_NEGATIVE_INT = { "type": int, "min": 0 }

_RELATIVE_PATH_LIST = { "type": list, "entry": { "type": bytes, "pattern": rb"[^/][^\x00]*" } }

SETTINGS = { "type": dict, "items": {
  "network": { "type": bool },

  "uid": _NON_NEGATIVE_INT,
  "cpu-period": _NON_NEGATIVE_INT,
  "cpu-quota": _NON_NEGATIVE_INT,
  "memory": _NON_NEGATIVE_INT,
  "disk-bps": _NON_NEGATIVE_INT,
  "disk-iops": _NON_NEGATIVE_INT,
  "nofile": _NON_NEGATIVE_INT,
  "locks": _NON_NEGATIVE_INT,
  "sigpending": _NON_NEGATIVE_INT,

  "certificate-identity": _PRINTABLE,
  "certificate-oidc-issuer": _PRINTABLE,
  "registry": _PRINTABLE,
  "sandbox-path": _ABSOLUTE_PATH,
  "disk-name": { "type": bytes, "pattern": rb"/dev/[^\x00]*" },
  "mount-parent": _ABSOLUTE_PATH,
  "working-dir": _ABSOLUTE_PATH,

  "volumes": { "type": dict, "items": {
    "read_write": _RELATIVE_PATH_LIST,
    "read_only": _RELATIVE_PATH_LIST,
    "tmpfs": _RELATIVE_PATH_LIST
  }},

  # from https://pubs.opengroup.org/onlinepubs/9799919799/
  "env": { "type": list, "entry": { "type": bytes, "pattern": rb"[^\x00=]+=[^\x00]*" } }
}}

VERIFY_OUTPUT = { "type": list, "entry": { "type": dict, "items": {
  "critical": { "type": dict, "strict": True, "items": {
    "type": _PRINTABLE_STRICT,

    "identity": { "type": dict },
    "image": { "type": dict, "strict": True, "items": {
      "docker-manifest-digest": _MANIFEST_DIGEST
    }}
  }},
  "optional": { "type": dict }
}}}

ATTEST_OUTPUT = { "type": dict, "items": {
  "payload": _PRINTABLE_STRICT,
  "payloadType": _PRINTABLE,

  "signatures": { "type": list }
}}

ATTEST_PAYLOAD = { "type": dict, "items": {
  "_type": _PRINTABLE,
  "predicateType": _PRINTABLE,

  "predicate": { "type": dict, "strict": True, "items": {
    "defaultAction": { "type": bytes, "strict": True, "pattern": rb"SCMP_ACT_ERRNO" },
    "defaultErrno": _PRINTABLE_STRICT,

    "architectures": { "type": list, "strict": True },
    "syscalls": { "type": list, "strict": True, "entry": { "type": dict, "items": {
      "errnoRet": _NON_NEGATIVE_INT,

      "action": { "type": bytes, "strict": True, "pattern": rb"(SCMP_ACT_ERRNO|SCMP_ACT_ALLOW)" },

      "names": { "type": list, "strict": True, "entry": _PRINTABLE },
      "args": { "type": list }
    }}}
  }},

  "subject": { "type": list }
}}

REFERENCE = { "type": dict, "items": {
  "registry": _PRINTABLE_STRICT,
  "digest": _MANIFEST_DIGEST
}}

DICT = { "type": dict }
