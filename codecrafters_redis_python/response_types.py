from typing import Protocol
from dataclasses import dataclass, field
from codecrafters_redis_python.constants import LINE_BREAK


@dataclass
class RespType(Protocol):
    content: str = ""

    def decode(self):
        pass


@dataclass
class RespSimpleString(RespType):
    content: str = ""

    def encode(self):
        content = f"${len(self.content)}{LINE_BREAK}{self.content}{LINE_BREAK}"
        return content.encode()


@dataclass
class RespBulkString(RespType):
    words: list[str] = field(default_factory=list)

    def encode(self):
        contents = []
        for word in self.words:
            contents.append(f"${len(word)}")
            contents.append(f"{word}")
        res = f"{LINE_BREAK}".join(contents)
        return (f"{res}{LINE_BREAK}").encode()


@dataclass
class RespPingPong(RespSimpleString):
    content: str = "PONG"


@dataclass
class RespNil(RespType):
    content: str = "$-1"

    def encode(self):
        return f"{self.content}{LINE_BREAK}".encode("utf8")


@dataclass
class RespOk(RespSimpleString):
    content: str = "OK"
