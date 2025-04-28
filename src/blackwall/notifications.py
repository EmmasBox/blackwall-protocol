
from textual.notifications import SeverityLevel

from blackwall.modals import generic_warning_modal
from blackwall.settings import get_user_setting


def send_notification(self,message: str, severity: SeverityLevel):
    if get_user_setting(section="notifications",setting="use_modal"):
        generic_warning_modal(self,modal_text=message)
    else:
        self.notify(message,severity=severity)