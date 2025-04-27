
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Button, Label, Input

class RvaryScreen(Screen):
    """Modal rvary password change screen"""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Change RVARY password", id="question"),
            Input(id="rvary_password",placeholder="enter password...",max_length=8),
            Input(id="rvary_password_confirm",placeholder="confirm password...",max_length=8),
            Button("Cancel", variant="primary", id="cancel", classes="modal-buttons"),
            Button("Confirm", variant="error", id="confirm", classes="modal-buttons"),
            id="dialog",
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            self.app.pop_screen()
            
        else:
            self.app.pop_screen()
