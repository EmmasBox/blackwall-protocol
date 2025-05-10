
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Button, Input, Label

from blackwall.api.setropts import racf_change_rvary_password


class RvaryScreen(Screen):
    """Modal rvary password change screen"""

    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Change RVARY password for whole RACF database. Password must be up to 8 characters long. Allowed characters: alphanumeric and @#$", id="question"),
            Input(id="rvary_password",restrict=r"([a-zA-Z]*[0-9]*[\@\#\$]*)",placeholder="enter password...",max_length=8,password=True),
            Input(id="rvary_password_confirm",restrict=r"([a-zA-Z]*[0-9]*[\@\#\$]*)",placeholder="confirm password...",max_length=8,password=True),
            Button("Cancel", variant="primary", id="cancel", classes="modal-buttons"),
            Button("Confirm", variant="error", id="confirm", classes="modal-buttons"),
            id="dialog",
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            input_value = self.query_exactly_one("#rvary_password",Input).value
            input_confirm_value = self.query_exactly_one("#rvary_password_confirm",Input).value
            if input_value == input_confirm_value:
                racf_change_rvary_password(input_value)
                self.app.pop_screen()
            else:
                self.notify("Password does not match",severity="error")
        else:
            self.app.pop_screen()
        self.query_exactly_one("#rvary_password",Input).value = ""
        self.query_exactly_one("#rvary_password_confirm",Input).value = ""
