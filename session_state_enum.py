def enum(**enums):
  return type('Enum', (), enums)

SessionState = enum(ADD="ADD", REMOVE="REMOVE", UNKNOWN='three')