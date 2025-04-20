
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Button

from blackwall.api.setropts import refresh_RACF
        
class RefreshScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Label("Refresh: ")
        yield Button("Refresh system",id="command_output_screen_log",action="refresh")
        yield Label("Press 'Esc' to exit refresh screen")
    
    def action_refresh(self):
        refresh_RACF()