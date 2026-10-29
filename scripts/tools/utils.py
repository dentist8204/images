import json
import os
from pathlib import Path
from re import findall
import subprocess
import sys

from errors import AppError, UsageError
import schema

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

def load_settings(container_name):
  if len(container_name) > 100:
    raise AppError("container name is too long")
  elif findall(r"[^a-zA-Z0-9\-_]", container_name):
    raise AppError("container name has invalid characters")

  user_settings = load_json("user_settings", f"{Path.home()}/.config/prun/settings.json",
                            schema.USER_SETTINGS)
  context_path  = f"{user_settings['context-path']}/{container_name}"
  settings      = load_json("settings", f"{context_path}/settings.json", schema.SETTINGS)

  return (user_settings, settings, context_path)

def load_json(name, file_path, schema_):
  with open(file_path, "r", encoding="utf-8") as file_:
    json_data = json.load(file_)

    check_structure(name, json_data, schema_)

    return json_data

def check_structure(name, data, schema_):
  if type(data) is not type(schema_):
    raise AppError(f"{name} is not a {type(schema_).__name__}")

  if isinstance(schema_, dict):
    for (key, expected_type) in schema_.items():
      if key not in data:
        raise AppError(f"{name}.{key} is missing")

      check_structure(f"{name}.{key}", data[key], expected_type)
  elif isinstance(schema_, list):
    for i in range(0, len(data)):
      check_structure(f"{name}[{i}]", data[i], schema_[0])

def run_main(main, tool_name):
  try:
    try:
      main()
    except KeyboardInterrupt:
      raise AppError("interrupted")
    except subprocess.CalledProcessError as e:
      raise AppError(e)
    except OSError as e:
      raise AppError(e)
  except AppError as e:
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
