# all terminal values in the following schemas are only there as examples and do not effect validation

USER_SETTINGS = {
  "registry": "ghcr.io/dentist8204/images",
  "certificate-identity": "https://github.com/dentist8204/images/.github/workflows/build-one.yml@refs/heads/main",
  "certificate-oidc-issuer": "https://token.actions.githubusercontent.com",
  "seccomp-config-path": "/home/user/repos/images/config/seccomp",
  "sandbox_path": "/home/user/.var/sandbox",
  "context_path": "/home/user/.local/share/prun",
  "tmpfs_path": "/home/user/.var/mnt/prun",
  "disk_name": "/dev/nvme0n1",
  "specs": {            # used for cgroups flags
    "cpus": 8,          # hardware threads, will be divided by 4
    "memory": 8192,     # total memory, will be divided by 4
    "disk-bps": 1024,   # disk throughput, will be divided by 8 for read and write
    "disk-iops": 250000 # random-4k iops, will be divided by 8 for read and write
  }
}

SETTINGS = {
  "usage": "age <encrypt|decrypt> [args...]",
  "network": False,
  "mount-parent": "/mnt",
  "working-dir": "/mnt/entry",
  "env": {},
  "volumes": {
    "read_write": [
      "entry"
    ],
    "read_only": [
      ".age"
    ]
  },
  "actions": {}
}

ENV = "/mnt/home"

ACTION = {
  "args_min": 2,
  "args_max": 2,
  "usage": "encrypt <output-file> <input-file>",
  "base_args": [
    "age",
    "-e",
    "-i",
    "/mnt/.age/key.txt",
    "-o"
  ]
}

VERIFY_OUTPUT = [
  {
    "critical": {
      "identity": {
        "docker-reference": "ghcr.io/dentist8204/images/age:latest"
      },
      "image": {
        "docker-manifest-digest": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
      },
      "type": "https://sigstore.dev/cosign/sign/v1"
    },
    "optional": {}
  },
  {
    "critical": {
      "identity": {
        "docker-reference": "ghcr.io/dentist8204/images/age:latest"
      },
      "image": {
        "docker-manifest-digest": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
      },
      "type": "https://seccomp-profile.local"
    },
    "optional": {}
  }
]

ATTEST_OUTPUT = {
  "payload": "base64-stuff",
  "payloadType": "application/vnd.in-toto+json",
  "signatures": [
    {
      "sig": "stuff"
    }
  ]
}

ATTEST_PAYLOAD = {
  "_type": "https://in-toto.io/Statement/v0.1",
  "subject": [
    {
      "name": "ghcr.io/dentist8204/images/age",
      "digest": {
        "sha256": "0000000000000000000000000000000000000000000000000000000000000000"
      }
    }
  ],
  "predicateType": "https://seccomp-profile.local",
  "predicate": {
    "architectures": [
      "SCMP_ARCH_X86_64"
    ],
    "defaultAction": "SCMP_ACT_ERRNO",
    "defaultErrno": "ENOSYS",
    "syscalls": [
      {
        "action": "SCMP_ACT_ALLOW",
        "names": [
          "arch_prctl"
        ]
      }
    ]
  }
}

ALLOWANCE    = {}
DENIALS      = {}
REPLACEMENTS = {}
SWAPS        = {}
