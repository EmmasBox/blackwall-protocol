
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Button, Label

class ModalScreen(Screen):
    """Modal screen"""

    def __init__(self, dialog_text: str, confirm_action: str):
        super().__init__()
        self.dialog_text = dialog_text
        self.confirm_action = confirm_action

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.dialog_text, id="question"),
            Button("Confirm", variant="error", id="confirm", classes="modal-buttons"),
            Button("Cancel", variant="primary", id="cancel", classes="modal-buttons"),
            id="dialog",
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            self.app.pop_screen()
            await self.app.run_action(self.confirm_action,default_namespace=self.parent)
        else:
            self.app.pop_screen()
