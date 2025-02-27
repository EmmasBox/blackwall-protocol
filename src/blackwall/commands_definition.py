class Positional:
    def __init__(self, positional: str):
        self.positional = positional

class Command:
    def __init__(self,command: str, short: str, alt: str, positionals: list[Positional]):
        self.command = command
        self.short = short
        self.alt = alt
        self.positionals = positionals

test_command = Command(command="TEST", short="T", alt="TE", positionals=[
    Positional("EMSE")
])