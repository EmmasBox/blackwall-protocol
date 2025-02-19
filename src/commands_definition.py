class Positional:
    def __init__(self, positional: str):
        self.positional = positional

class Command:
    def __init__(self,type: str,command: str, short: str, alt: str, positionals: list[Positional]):
        self.type = type
        self.command = command
        self.short = short
        self.alt = alt
        self.positionals = positionals

test_command = Command("TEST", short="T", alt="TE", positional=[
    Positional("EMSE")
])