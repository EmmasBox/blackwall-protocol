
from textual.widget import Widget

from blackwall.screens.modal.modal import ModalScreen

def generic_confirmation_modal(self, modal_text: str, confirm_action: str, action_widget: Widget) -> None:
    modal_screen = ModalScreen(dialog_text=modal_text,confirm_action=confirm_action,action_widget=action_widget)

    self.app.push_screen(modal_screen)