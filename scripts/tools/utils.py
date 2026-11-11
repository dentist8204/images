import json
import os
from pathlib import Path
import re
import subprocess
import sys

from errors import AppError, UsageError
import schema

defaults = {
  "uid": 1007,
  "cpu-period": 100000, # micro-seconds
  "cpu-quota": 400000,  # micro-seconds
  "memory": 4096,       # mebi-bytes
  "disk-bps": 256,      # mebi-bytes
  "disk-iops": 50000,   # read or write operations

  "registry": "ghcr.io/dentist8204/images",
  "certificate-identity": "https://github.com/dentist8204/images/.github/workflows/build-one.yml@refs/heads/main",
  "certificate-oidc-issuer": "https://token.actions.githubusercontent.com"
}

def load_settings(container_name):
  if len(container_name) > 100:
    raise AppError("container name is too long")
  elif len(container_name) < 1:
    raise AppError("container name is too short")
  # https://specs.opencontainers.org/distribution-spec/#DISTRIBUTION-SPEC-27
  elif not re.fullmatch(r"[a-z0-9]+((\.|_|__|-+)[a-z0-9]+)*", container_name):
    raise AppError("container name is invalid")

  home_path = Path.home()

  user_settings = load_json("user_settings", home_path / ".config" / "prun" / "settings.json",
                            schema.USER_SETTINGS)
  context_path  = home_path / ".local" / "share" / "prun" / container_name
  settings      = load_json("settings", context_path / "settings.json", schema.SETTINGS)

  return (user_settings, settings, context_path)

def load_json(name, file_path, schema_):
  with open(file_path, "r", encoding="utf-8") as file_:
    try:
      json_data = json.load(file_)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
      raise AppError(f"{file_path}: {e}")

    check_structure(name, json_data, schema_)

    return json_data

def validate_data(name, data, schema_):
  if isinstance(data, str):
    data = data.encode("utf-8")

  required_type = schema_["type"]

  if not isinstance(data, required_type):
    raise AppError(f"{name} is not type {required_type.__name__}")

  match data:
    case dict():
      if "items" in schema_:
        items_schema = schema_["items"]

        for (key, value) in items_schema.items():
          if value["strict"] and key not in data:
            raise AppError(f"{name}.{key} is missing")

        for (key, value) in data.items():
          if key not in schema_:
            raise AppError(f"{name}.{key} is an unknown key")

          validate_data(f"{name}.{key}", value, items_schema[key])
   case list():
     if "entry" in schema_:
       entry_schema = schema_["entry"]

       for (i, entry) in enumerate(data):
         validate_data(f"{name}[{i}]", entry, entry_schema)
   case int():
     if "min" in schema_ and data < schema_["min"]:
       raise AppError(f"{name} < {schema_['min']}")
   case bytes():
     if "pattern" in schema_ and not re.fullmatch(schema_["pattern"], data):
       raise AppError(f"{name} does not match regex")

def run_main(main, tool_name):
  try:
    try:
      main()
    except KeyboardInterrupt:
      raise AppError("interrupted")
  except (AppError, OSError, subprocess.CalledProcessError) as e:
    print(f"{tool_name}:", e, file=sys.stderr)
    sys.exit(1)
  except UsageError as e:
    print(f"usage: {tool_name}", e, file=sys.stderr)
    sys.exit(2)

def get_value(key, user_settings, settings=None):
  if settings is not None and key in settings:
    return settings[key]

  if key in user_settings:
    return user_settings[key]

  return defaults[key]
