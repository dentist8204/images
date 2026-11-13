import re

from errors import AppError

class Schema:
  def __init__(self, type_=object, strict=False):
    self.type_ = type_
    self.strict = strict

  def validate(self, name, data):
    if not isinstance(data, self.type_):
      raise AppError(f"{name} is not type {self.type_.__name__}")

class IntSchema(Schema):
  def __init__(self, min_=None, **kwargs):
    super().__init__(type_=int, **kwargs)

    self.min_ = min_

  def validate(self, name, data):
    super().validate(name, data)

    if self.min_ is not None and data < self.min_:
      raise AppError(f"{name} < {self.min_}")

class StringSchema(Schema):
  def __init__(self, pattern=None, **kwargs):
    super().__init__(type_=str, **kwargs)

    self.pattern = pattern

  def validate(self, name, data):
    super().validate(name, data)

    if self.pattern and not re.fullmatch(self.pattern, data):
      raise AppError(f"{name} does not match {self.pattern}")

class DictSchema(Schema):
  def __init__(self, items=None, **kwargs):
    super().__init__(type_=dict, **kwargs)

    self.items = items

  def validate(self, name, data):
    super().validate(name, data)

    if self.items:
      for (key, schema_) in self.items.items():
        if schema_.strict and key not in data:
          raise AppError(f"{name}.{key} is missing")

      for (key, value) in data.items():
        if key not in self.items:
          raise AppError(f"{name}.{key} is an unknown key")

        self.items[key].validate(f"{name}.{key}", value)

class ListSchema(Schema):
  def __init__(self, entry_schema=None, **kwargs):
    super().__init__(type_=list, **kwargs)

    self.entry_schema = entry_schema

  def validate(self, name, data):
    super().validate(name, data)

    if self.entry_schema:
      for (i, entry) in enumerate(data):
        self.entry_schema.validate(f"{name}[{i}]", entry)

__ONE_OR_MORE_VISIBLE = r"[!-~]+"
__ABSOLUTE_PATH       = r"/[^\u0000]*"
__RELATIVE_PATH       = r"[^/][^\u0000]*"
__ENV                 = r"[^\u0000=]+=[^\u0000]*"
__ERRNO               = r"SCMP_ACT_ERRNO"
# from https://github.com/opencontainers/image-spec/blob/13cff54902ec9ad6320cbc487a685b66fcd67171/descriptor.md#digests
__MANIFEST_DIGEST     = r"[a-z0-9]+([+._-][a-z0-9]+)*:[a-zA-Z0-9=_-]+"

__DEVICE_PATH    = rf"/dev{__ABSOLUTE_PATH}"
__ERRNO_OR_ALLOW = rf"({__ERRNO}|SCMP_ACT_ALLOW)"

_NON_NEGATIVE_INT = IntSchema(min_=0)

_ABSOLUTE_PATH   = StringSchema(pattern=__ABSOLUTE_PATH)
_VISIBLE         = StringSchema(pattern=__ONE_OR_MORE_VISIBLE)
_VISIBLE_STRICT  = StringSchema(pattern=__ONE_OR_MORE_VISIBLE, strict=True)

_RELATIVE_PATH_LIST = ListSchema(entry_schema=StringSchema(pattern=__RELATIVE_PATH))

SETTINGS = DictSchema(items={
  "network": Schema(type_=bool),

  "uid": _NON_NEGATIVE_INT,
  "cpu-period": _NON_NEGATIVE_INT,
  "cpu-quota": _NON_NEGATIVE_INT,
  "memory": _NON_NEGATIVE_INT,
  "disk-bps": _NON_NEGATIVE_INT,
  "disk-iops": _NON_NEGATIVE_INT,
  "nofile": _NON_NEGATIVE_INT,
  "locks": _NON_NEGATIVE_INT,
  "sigpending": _NON_NEGATIVE_INT,

  "certificate-identity": _VISIBLE,
  "certificate-oidc-issuer": _VISIBLE,
  "registry": _VISIBLE,
  "sandbox-path": _ABSOLUTE_PATH,
  "disk-name": StringSchema(pattern=__DEVICE_PATH),
  "mount-parent": _ABSOLUTE_PATH,
  "working-dir": _ABSOLUTE_PATH,

  "volumes": DictSchema(items={
    "read-write": _RELATIVE_PATH_LIST,
    "read-only": _RELATIVE_PATH_LIST,
    "tmpfs": _RELATIVE_PATH_LIST
  }),

  "env": ListSchema(entry_schema=StringSchema(pattern=__ENV))
})

VERIFY_OUTPUT = ListSchema(entry_schema=DictSchema(items={
  "critical": DictSchema(strict=True, items={
    "type": _VISIBLE_STRICT,

    "identity": DictSchema(),
    "image": DictSchema(strict=True, items={
      "docker-manifest-digest": StringSchema(pattern=__MANIFEST_DIGEST, strict=True)
    })
  }),
  "optional": DictSchema()
}))

ATTEST_OUTPUT = DictSchema(items={
  "payload": _VISIBLE_STRICT,
  "payloadType": _VISIBLE,

  "signatures": ListSchema()
})

ATTEST_PAYLOAD = DictSchema(items={
  "_type": _VISIBLE,
  "predicateType": _VISIBLE,

  "predicate": DictSchema(strict=True, items={
    "defaultAction": StringSchema(pattern=__ERRNO, strict=True),
    "defaultErrno": _VISIBLE_STRICT,

    "architectures": ListSchema(strict=True),
    "syscalls": ListSchema(strict=True, entry_schema=DictSchema(items={
      "errnoRet": _NON_NEGATIVE_INT,

      "action": StringSchema(pattern=__ERRNO_OR_ALLOW, strict=True),

      "names": ListSchema(strict=True, entry_schema=_VISIBLE),
      "args": ListSchema()
    }))
  }),

  "subject": ListSchema()
})

REFERENCE = DictSchema(items={
  "registry": _VISIBLE_STRICT,
  "digest": StringSchema(pattern=__MANIFEST_DIGEST, strict=True)
})

DICT = DictSchema()
