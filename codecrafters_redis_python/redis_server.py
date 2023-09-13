import socket
import threading
from codecrafters_redis_python.commands import (
    CommandPingPong,
    CommandEcho,
    CommandSet,
    CommandGet,
)
from codecrafters_redis_python.constants import LINE_BREAK
from codecrafters_redis_python.factories import CommandsFactory


class StorageSet(dict):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = dict.__new__(cls, *args, **kwargs)

        return cls._instance


class RedisServer:
    def __init__(self, host, port, storage) -> None:
        self.host = host
        self.port = port
        self.storage = storage
        self.command_factory = CommandsFactory()
        self.command_factory.register_command("ping", CommandPingPong)
        self.command_factory.register_command("echo", CommandEcho)
        self.command_factory.register_command("set", CommandSet)
        self.command_factory.register_command("get", CommandGet)

    def run(self):
        server_socket = socket.create_server((self.host, self.port), reuse_port=True)
        for _ in range(20):
            x = threading.Thread(target=self.execute_process, args=(server_socket,))
            x.start()

    def execute_process(self, server_socket):
        conn, _ = server_socket.accept()
        while conn:
            data = conn.recv(1024).decode()
            partials = list(filter(None, data.split(LINE_BREAK)))

            if not partials:
                return
            current_command = partials[2]
            current_arguments = partials[4::2]
            try:
                command = self.command_factory.create(
                    current_command,
                    **{
                        "server": self,
                        "connection": conn,
                        "arguments": current_arguments,
                    }
                )
                command.run()
            except Exception:
                raise Exception("Not Implemented")
