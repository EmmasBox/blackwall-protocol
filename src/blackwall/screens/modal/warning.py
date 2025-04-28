
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Button, Label


class WarningScreen(Screen):
    """Warning screen"""

    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def __init__(self, dialog_text: str):
        super().__init__()
        self.dialog_text = dialog_text

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.dialog_text, id="question"),
            Button("Dismiss", variant="warning", id="dismiss", classes="single-modal-button"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()