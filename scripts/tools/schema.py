# all terminal values in the following schemas are only there as examples and do not effect validation

USER_SETTINGS = {
  "sandbox-path": "/home/user/.var/sandbox",
  "tmpfs-path": "/home/user/.var/mnt/prun", # needs a safe size and inode limit
  "disk-name": "/dev/nvme0n1"
}

SETTINGS = {
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
  }
}

ENV = "/mnt/home"

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

REFERENCE = {
  "registry": "ghcr.io/dentist8204/images",
  "digest": "sha256:0000000000000000000000000000000000000000000000000000000000000000"
}

A_DICT = {}
