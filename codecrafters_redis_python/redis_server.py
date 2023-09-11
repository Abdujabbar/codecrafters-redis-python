import socket
import threading
from codecrafters_redis_python.commands import (
    CommandPingPong,
    CommandEcho,
    CommandSet,
    CommandGet,
)


class StorageSet(dict):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = dict.__new__(cls, *args, **kwargs)

        return cls._instance


class RedisServer:
    OPERATION_COMMANDS = {
        "ping": CommandPingPong,
        "echo": CommandEcho,
        "set": CommandSet,
        "get": CommandGet,
    }

    def __init__(self, host, port, storage) -> None:
        self.host = host
        self.port = port
        self.storage = storage

    def run(self):
        server_socket = socket.create_server((self.host, self.port),
                                             reuse_port=True)
        for _ in range(20):
            x = threading.Thread(target=self.execute_process,
                                 args=(server_socket,))
            x.start()

    def execute_process(self, server_socket):
        conn, _ = server_socket.accept()
        while conn:
            data = conn.recv(1024).decode()
            partials = list(filter(None, data.split("\r\n")))

            if not partials:
                return
            current_command = partials[2]
            current_arguments = partials[4::2]

            if current_command in self.OPERATION_COMMANDS:
                self.OPERATION_COMMANDS[current_command](
                    self, conn, current_arguments
                ).run()
            else:
                raise Exception("Not Implemented")
