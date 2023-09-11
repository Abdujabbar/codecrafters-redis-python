from typing import Protocol
from dataclasses import dataclass, field


@dataclass
class RespType(Protocol):
    content: str = ""

    def decode(self):
        pass


@dataclass
class RespSimpleString(RespType):
    content: str = ""

    def encode(self):
        return f"${len(self.content)}\r\n{self.content}\r\n".encode()


@dataclass
class RespBulkString(RespType):
    words: list[str] = field(default_factory=list)

    def encode(self):
        contents = []
        for word in self.words:
            contents.append(f"${len(word)}")
            contents.append(f"{word}")

        return ("\r\n".join(contents) + "\r\n").encode()


@dataclass
class RespPingPong(RespSimpleString):
    content: str = "PONG"


@dataclass
class RespNil(RespType):
    content: str = "$-1"

    def encode(self):
        return f"{self.content}\r\n".encode("utf8")


@dataclass
class RespOk(RespSimpleString):
    content: str = "OK"

    def encode(self):
        return f"${len(self.content)}\r\n{self.content}\r\n".encode()
