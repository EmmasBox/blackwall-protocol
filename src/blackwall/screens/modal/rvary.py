
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Button, Label, Input

class RvaryScreen(Screen):
    """Modal rvary password change screen"""

    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Change RVARY password for whole RACF database. Password must be up to 8 characters long. Only do this if you're absolutely sure you know what you're doing.", id="question"),
            Input(id="rvary_password",placeholder="enter password...",max_length=8,password=True),
            Input(id="rvary_password_confirm",placeholder="confirm password...",max_length=8,password=True),
            Button("Cancel", variant="primary", id="cancel", classes="modal-buttons"),
            Button("Confirm", variant="error", id="confirm", classes="modal-buttons"),
            id="dialog",
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            input_value = self.get_child_by_id("rvary_password",Input).value
            input_confirm_value = self.get_child_by_id("rvary_password_confirm",Input).value
            if input_value == input_confirm_value:
                self.app.pop_screen()
        else:
            self.app.pop_screen()
