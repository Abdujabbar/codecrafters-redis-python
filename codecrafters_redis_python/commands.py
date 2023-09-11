import time
from codecrafters_redis_python.response_types import (
    RespPingPong,
    RespSimpleString,
    RespBulkString,
    RespOk,
    RespNil,
)
from codecrafters_redis_python.exceptions import (
    KeyNotFoundException,
    KeyAlreadyExpiredException,
)


class Command:
    def __init__(self, server, connection, arguments) -> None:
        self.arguments = arguments
        self.connection = connection
        self.server = server

    def run():
        pass


class CommandPingPong(Command):
    def run(self):
        self.connection.send(RespPingPong().encode())


class CommandEcho(Command):
    def run(self):
        self.connection.send(RespBulkString(words=self.arguments).encode())


class CommandSet(Command):
    def run(self):
        try:
            self.process_args(self.arguments)
            self.connection.send(RespOk().encode())
        except Exception as ex:
            self.connection.send(RespSimpleString(content=str(ex)).encode())

    def process_args(self, arguments):
        expire = -1
        if len(arguments) >= 4:
            if arguments[-2].lower() != "px":
                raise ValueError(f"Wrong command: {arguments[-2]}")
            if arguments[-2].lower() == "px":
                expire = int(arguments[-1]) / 1000

        key = arguments[0]
        value = arguments[1]
        self.server.storage[key] = (value, expire, time.time())


class CommandGet(Command):
    def run(self):
        try:
            result = self.process_args(self.arguments)
            self.connection.send(RespSimpleString(content=result).encode())
        except (KeyAlreadyExpiredException, KeyNotFoundException):
            self.connection.send(RespNil().encode())

    def process_args(self, arguments):
        key = arguments[-1]
        if key not in self.server.storage:
            raise KeyNotFoundException()

        value, expire, prev_time = self.server.storage.get(key)
        if expire != -1:
            curr_time = time.time()

            if curr_time - prev_time > expire:
                raise KeyAlreadyExpiredException()

        return value
