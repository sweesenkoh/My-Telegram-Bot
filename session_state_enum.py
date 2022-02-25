def enum(**enums):
  return type('Enum', (), enums)

SessionState = enum(ADD="ADD", REMOVE="REMOVE", CHECK="CHECK", UNKNOWN='three')