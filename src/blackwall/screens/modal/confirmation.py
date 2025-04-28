
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Button, Label


class ConfirmationScreen(Screen):
    """Modal confirmation screen"""

    def __init__(self, dialog_text: str, confirm_action: str,action_widget: Widget):
        super().__init__()
        self.dialog_text = dialog_text
        self.confirm_action = confirm_action
        self.action_widget = action_widget

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(self.dialog_text, id="question"),
            Button("Cancel", variant="primary", id="cancel", classes="modal-buttons"),
            Button("Confirm", variant="error", id="confirm", classes="modal-buttons"),
            id="dialog",
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            self.app.pop_screen()
            await self.app.run_action(self.confirm_action,default_namespace=self.action_widget)
        else:
            self.app.pop_screen()
