
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Button
from textual.containers import Grid

from blackwall.api.setropts import refresh_RACF
        
class RefreshScreen(Screen):
    """Refresh RACF database screen"""

    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to issue a refresh of the system?", id="question"),
            Button("Cancel", variant="primary", id="cancel", classes="modal-buttons"),
            Button("Confirm", variant="error", id="confirm", classes="modal-buttons"),
            id="dialog",
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            return_code = refresh_RACF()
            if return_code == 0:
                self.notify(f"Refresh successfully issued, return code: {return_code}",severity="information")
            else:
                self.notify(f"Refresh failed, return code: {return_code}",severity="error")
            self.app.pop_screen()
        else:
            self.app.pop_screen()
