from textual.message import Message
from textual.widget import Widget


class OpenTab(Message):
    def __init__(self, title: str, content: Widget):
        super().__init__()
        self.title =  title
        self.content = content

class SubmitCommand(Message):
    def __init__(self, command: str):
        super().__init__()
        self.command =  command

class SubmitError(Message):
    def __init__(self, error: str):
        super().__init__()
        self.error = error