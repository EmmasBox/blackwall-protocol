from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import VerticalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import DataTable, Input, Label

from blackwall.api import keyrings
from blackwall.panels.traits_ui import set_traits_in_input

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
    keyring_name: str = ""
    keyring_owner: str = ""
    keyring_traits: keyrings.KeyringTraits | None = None
    certificate_traits: keyrings.CertificateTraits | None = None

class PanelKeyring(VerticalScroll):

    keyring_info: reactive[KeyringInfo] = reactive(KeyringInfo())

    def on_mount(self) -> None:
        if keyrings.keyring_exists(keyring=self.keyring_info.keyring_name,owner=self.keyring_info.keyring_owner):
            self.query_exactly_one("#ring_name",Input).value = self.keyring_info.keyring_name.upper()
            self.query_exactly_one("#ring_owner",Input).value = self.keyring_info.keyring_name.upper()
            
            if self.keyring_info.certificate_traits is not None:
                set_traits_in_input(self,traits=self.keyring_info.certificate_traits,prefix="certificates")

    def compose(self) -> ComposeResult:
        yield PanelKeyringInfo()
        yield PanelKeyringCertificates()