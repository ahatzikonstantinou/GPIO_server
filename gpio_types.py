from enum import Enum
from typing import TypedDict

class Direction(str, Enum):
    IN = "in"
    OUT = "out"

class Command(str, Enum):
    REQUEST = "request"
    RELEASE = "release"
    WRITE = "write"
    READ = "read"
    CHECK = "check"
    PIN_INFO = "getPinInfo"
    ALL_PINS_INFO = "getAllPinsInfo"

class PinRequest(TypedDict):
    command: str
    pin: int
    direction: str
    client_id: str

class PinWrite(TypedDict):
    command: str
    pin: int
    value: int
    client_id: str

class PinRelease(TypedDict):
    command: str
    pin: int
    client_id: str

class DebugRequest(TypedDict):
    command: str
    pin: int | None
