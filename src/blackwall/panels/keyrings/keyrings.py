from dataclasses import dataclass

from textual.app import ComposeResult
from textual.containers import VerticalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import DataTable, Input, Label

from blackwall.api import keyrings

CERTIFICATE_COLUMNS = [
    ("DN", "Owner", "Issuer", "Key size", "Valid after", "Valid before"),
]

@dataclass
class KeyringInfo:
    keyring_name: str = ""
    keyring_owner: str = ""
    keyring_traits: keyrings.KeyringTraits | None = None


class PanelKeyringInfo(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Keyring: ")
        yield Input(id="ring_name",disabled=True)
        yield Label("Owner: ")
        yield Input(id="ring_owner",max_length=8,classes="field-short-generic",disabled=True)

class PanelKeyringCertificates(VerticalGroup):

    def __init__(self, keyring_info: KeyringInfo):
        super().__init__()
        self.keyring_info = keyring_info

    def compose(self) -> ComposeResult:
        yield Label("certificates: ")
        yield DataTable(id="certificates_table")

    def on_mount(self) -> None:
        certificates_table = self.get_child_by_id("certificates_table",DataTable)
        certificates_table.zebra_stripes = True
        certificates_table.add_columns(*CERTIFICATE_COLUMNS[0]) 

        self.notify(self.keyring_info.keyring_name)
        if self.keyring_info.keyring_traits is not None:
            self.notify("blep")
        if self.keyring_info.keyring_traits is not None and self.keyring_info.keyring_traits.certificates is not None:
            self.notify("debug")
            for certificate in self.keyring_info.keyring_traits.certificates:

                certificates_table.add_row(certificate.DN,certificate.owner,certificate.issuer,certificate.keySize,certificate,certificate.notBefore,certificate.notAfter)

class PanelKeyring(VerticalScroll):

    keyring_info: reactive[KeyringInfo] = reactive(KeyringInfo())

    def on_mount(self) -> None:
        if keyrings.keyring_exists(keyring=self.keyring_info.keyring_name,owner=self.keyring_info.keyring_owner):
            self.query_exactly_one("#ring_name",Input).value = self.keyring_info.keyring_name.upper()
            self.query_exactly_one("#ring_owner",Input).value = self.keyring_info.keyring_name.upper()

    def compose(self) -> ComposeResult:
        yield PanelKeyringInfo()
        yield PanelKeyringCertificates(keyring_info=self.keyring_info)