import json
import os
from pathlib import Path
from re import findall
import subprocess

from errors import AppError, UsageError
import schema

def load_settings(container_name):
  if len(container_name) > 100:
    raise AppError("container name is too long")
  elif findall(r"[^a-zA-Z0-9-_]", container_name):
    raise AppError("container name has invalid characters")

  user_settings = load_json(f"{Path.home()}/.config/prun/settings.json")

  check_structure("user_settings", user_settings, schema.USER_SETTINGS)

  context_path = f"{user_settings['context_path']}/{container_name}"
  settings     = load_json(f"{context_path}/settings.json")

  check_structure("settings", settings, schema.SETTINGS)

  return (user_settings, settings, context_path)

def load_json(file_path):
  try:
    with open(file_path, "r", encoding="utf-8") as file_:
      return json.load(file_)
  except (FileNotFoundError, IsADirectoryError, NotADirectoryError, PermissionError) as e:
    raise AppError(e)

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
