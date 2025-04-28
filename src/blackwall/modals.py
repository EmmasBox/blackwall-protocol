
from textual.widget import Widget

from blackwall.screens.modal.confirmation import ConfirmationScreen
from blackwall.screens.modal.warning import WarningScreen


def generic_confirmation_modal(self: Widget, modal_text: str, confirm_action: str, action_widget: Widget) -> None:
    modal_screen = ConfirmationScreen(dialog_text=modal_text,confirm_action=confirm_action,action_widget=action_widget)

    self.app.push_screen(modal_screen)

def generic_warning_modal(self: Widget, modal_text: str) -> None:
    modal_screen = WarningScreen(dialog_text=modal_text)

    self.app.push_screen(modal_screen)