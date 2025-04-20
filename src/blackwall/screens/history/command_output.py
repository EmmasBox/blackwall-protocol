
from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.signal import Signal
from textual.events import ScreenResume
from textual.containers import VerticalGroup
from textual.widgets import Log, Label

class CommandOutputWidget(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Command history: ")
        yield Log(id="command_output_screen_log")
        yield Label("Press 'Esc' to exit command history")

class CommandOutputScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield CommandOutputWidget()
    #command_output_change
    @on(ScreenResume)
    def on_resume(self):
        on_change: Signal[str] = self.app.command_output_change # type: ignore
        on_change.subscribe(node=self,callback=self.write_to_log)
        self.write_to_log(self.app.command_output) # type: ignore
    
    def write_to_log(self, output: str):
        log = self.get_child_by_id("command_output_screen_log",Log)
        log.clear()
        log.write(output)