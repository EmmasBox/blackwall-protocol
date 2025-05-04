from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import VerticalGroup, VerticalScroll
from textual.widgets import DataTable, Input, Label

from blackwall.api import keyrings


class PanelKeyringInfo(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Keyring: ")
        yield Input(id="ring_name",disabled=True)
        yield Label("Owner: ")
        yield Input(id="ring_owner",max_length=8,classes="field-short-generic",disabled=True)

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