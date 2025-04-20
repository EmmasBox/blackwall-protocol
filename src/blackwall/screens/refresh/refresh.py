
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Button
from textual.containers import Middle, Center

from blackwall.api.setropts import refresh_RACF
        
class RefreshScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    async def action_refresh(self) -> None:
        return_code = refresh_RACF()
        if return_code == 0:
            self.notify(f"Refresh successfully issued, return code: {return_code}",severity="information")
        else:
            self.notify(f"Refresh failed, return code: {return_code}",severity="error")
    
    def compose(self) -> ComposeResult:
        self.styles.opacity = "50%"
        with Middle():
            with Center():
                yield Label("Here you can issue a refresh of the system")
                yield Button("Refresh system",variant="warning",action="refresh")
                yield Label("Press 'Esc' to exit refresh screen")