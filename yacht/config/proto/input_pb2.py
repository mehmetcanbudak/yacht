# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yacht/config/proto/input.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='yacht/config/proto/input.proto',
  package='yacht.config.proto',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1eyacht/config/proto/input.proto\x12\x12yacht.config.proto\"\x96\x02\n\x0bInputConfig\x12\x0e\n\x06market\x18\x01 \x01(\t\x12\x0f\n\x07\x64\x61taset\x18\x02 \x01(\t\x12\x18\n\x10price_normalizer\x18\x03 \x01(\t\x12\x18\n\x10other_normalizer\x18\x04 \x01(\t\x12\x0b\n\x03\x65nv\x18\x05 \x01(\t\x12\x0f\n\x07tickers\x18\x06 \x03(\t\x12\x11\n\tintervals\x18\x07 \x03(\t\x12\x10\n\x08\x66\x65\x61tures\x18\x08 \x03(\t\x12\r\n\x05start\x18\t \x01(\t\x12\x0b\n\x03\x65nd\x18\n \x01(\t\x12\x1d\n\x15\x62\x61\x63k_test_split_ratio\x18\x0b \x01(\x02\x12\x1f\n\x17\x62\x61\x63k_test_embargo_ratio\x18\x0c \x01(\x02\x12\x13\n\x0bwindow_size\x18\r \x01(\x05\x62\x06proto3')
)




_INPUTCONFIG = _descriptor.Descriptor(
  name='InputConfig',
  full_name='yacht.config.proto.InputConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='market', full_name='yacht.config.proto.InputConfig.market', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='dataset', full_name='yacht.config.proto.InputConfig.dataset', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='price_normalizer', full_name='yacht.config.proto.InputConfig.price_normalizer', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='other_normalizer', full_name='yacht.config.proto.InputConfig.other_normalizer', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='env', full_name='yacht.config.proto.InputConfig.env', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tickers', full_name='yacht.config.proto.InputConfig.tickers', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='intervals', full_name='yacht.config.proto.InputConfig.intervals', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='features', full_name='yacht.config.proto.InputConfig.features', index=7,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start', full_name='yacht.config.proto.InputConfig.start', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end', full_name='yacht.config.proto.InputConfig.end', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='back_test_split_ratio', full_name='yacht.config.proto.InputConfig.back_test_split_ratio', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='back_test_embargo_ratio', full_name='yacht.config.proto.InputConfig.back_test_embargo_ratio', index=11,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='window_size', full_name='yacht.config.proto.InputConfig.window_size', index=12,
      number=13, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=55,
  serialized_end=333,
)

DESCRIPTOR.message_types_by_name['InputConfig'] = _INPUTCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

InputConfig = _reflection.GeneratedProtocolMessageType('InputConfig', (_message.Message,), dict(
  DESCRIPTOR = _INPUTCONFIG,
  __module__ = 'yacht.config.proto.input_pb2'
  # @@protoc_insertion_point(class_scope:yacht.config.proto.InputConfig)
  ))
_sym_db.RegisterMessage(InputConfig)


# @@protoc_insertion_point(module_scope)
