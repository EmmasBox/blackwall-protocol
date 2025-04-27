
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, Button
from textual.containers import Grid

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
        yield Grid(
            Label("Here you can issue a refresh of the system", id="question"),
            Button("Cancel", variant="primary", id="cancel", classes="modal-buttons"),
            Button("Confirm", variant="error", id="confirm", classes="modal-buttons"),
            id="dialog",
        )