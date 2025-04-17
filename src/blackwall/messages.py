from textual.widget import Widget
from textual.message import Message

class OpenTab(Message):
    def __init__(self, title: str, content: Widget):
        super().__init__()
        self.title =  title
        self.content = content

class SubmitCommand(Message):
    def __init__(self, command: str):
        super().__init__()
        self.command =  command