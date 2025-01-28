class Command:
    def __init__(self,command: str, short: str, alt: str):
        self.command = command
        self.short = short
        self.alt = alt

class Positional:
    def __init__(self,positional: str, parent: str):
        self.positional = positional
        self.parent = parent