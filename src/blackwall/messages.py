from textual.widget import Widget
from textual.message import Message

class OpenTab(Message):
    def __init__(self, title: str, content: Widget):
        super().__init__()
        self.title =  title
        self.content = content

class CommandHistory(Message):
    def __init__(self, history: str):
        super().__init__()
        self.history =  history