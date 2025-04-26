
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
            Button("Confirm", variant="error", id="confirm"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            await self.app.pop_screen()
            await self.app.run_action(self.confirm_action,default_namespace=self.parent)
        else:
            await self.app.pop_screen()
