from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import VerticalGroup, VerticalScroll
from textual.widgets import DataTable, Input, Label

from blackwall.api import keyrings

CERTIFICATE_COLUMNS = [
    ("DN", "Owner", "Issuer", "Key size", "Valid after", "Valid before"),
]

class PanelKeyringInfo(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Keyring: ")
        yield Input(id="ring_name",disabled=True)
        yield Label("Owner: ")
        yield Input(id="ring_owner",max_length=8,classes="field-short-generic",disabled=True)

class PanelKeyringCertificates(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("certificates: ")
        yield DataTable(id="certificates_table")

    def on_mount(self) -> None:
        certificates_table = self.get_child_by_id("certificates_table",DataTable)
        certificates_table.zebra_stripes = True
        certificates_table.add_columns(*CERTIFICATE_COLUMNS[0]) 


@dataclass
class KeyringInfo:
    keyring_traits: keyrings.KeyringTraits 
    certificate_traits: keyrings.CertificateTraits

class PanelKeyring(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelKeyringInfo()
        yield PanelKeyringCertificates()