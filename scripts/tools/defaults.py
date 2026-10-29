defaults = {
  "uid": 1007,
  "cpu-period": 100000,
  "cpu-qouta": 400000,
  "memory": 4096,       # mebibytes
  "disk-bps": 256,      # mebibytes
  "disk-iops": 50000,
  "hardlinks-max": 20,  # prevent hardlink bombs

  "registry": "ghcr.io/dentist8204/images",
  "certificate-identity": "https://github.com/dentist8204/images/.github/workflows/build-one.yml@refs/heads/main",
  "certificate-oidc-issuer": "https://token.actions.githubusercontent.com"
}
