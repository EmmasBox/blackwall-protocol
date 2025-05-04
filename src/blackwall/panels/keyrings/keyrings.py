from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import DataTable, Input, Label

from blackwall.api import keyrings


class PanelKeyringInfo(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Keyring: ")
        yield Input(id="ring_name")

class PanelKeyringCertificates(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("certificates: ")
        yield DataTable()

@dataclass
class KeyringInfo:
    keyring_traits: keyrings.KeyringTraits 
    certificate_traits: keyrings.CertificateTraits

class PanelKeyring(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelKeyringInfo()
        yield PanelKeyringCertificates()