class CommandsFactory:
    def __init__(self) -> None:
        self.builders = {}

    def register_command(self, command, builder, **kwargs):
        self.builders[command] = builder

    def create(self, key, **kwargs):
        builder = self.builders.get(key)

        if not builder:
            raise ValueError("Invalid command")

        return builder(**kwargs)
