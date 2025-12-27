
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import DataTable, Input, Label, Select

from blackwall.api.rrsf import (
    BaseRRSFTraits,
    get_rrsf_options,
)

RRSF_COLUMNS = [
    ("Node","System name", "Description", "State", "Protocol","Requests denied"),
]


class PanelRRSFNodes(VerticalGroup):
    base_traits: reactive[BaseRRSFTraits] = reactive(BaseRRSFTraits())

    def on_mount(self) -> None:
        rrsf_table = self.get_child_by_id("rrsf_nodes_table",DataTable)
        rrsf_table.zebra_stripes = True
        rrsf_table.add_columns(*RRSF_COLUMNS[0]) 

    def watch_base_traits(self):
        if self.base_traits.nodes is not None:
            rrsf_table = self.get_child_by_id("rrsf_nodes_table",DataTable)

            for node in self.base_traits.nodes:
                rrsf_table.add_row(
                    node["base:node_name"] or "",
                    node["base:multisystem_node_name"] or "",
                    node["base:node_description"],
                    str(node["base:node_state"] or ""),
                    node["base:node_protocol"] or "",
                    str(node["base:requests_denied"] or ""),
                    )

    def compose(self) -> ComposeResult:
        yield Label("RRSF Nodes", classes="rrsf-label")
        yield DataTable(id="rrsf_nodes_table")

class PanelRRSFMetaData(HorizontalGroup):
    base_traits: reactive[BaseRRSFTraits] = reactive(BaseRRSFTraits())

    def on_mount(self) -> None:
        if self.base_traits.subsystem_name is not None:
            self.notify(self.base_traits.subsystem_name)

    def watch_base_traits(self):
        if self.base_traits.subsystem_name is not None:
            self.get_child_by_id(id="rrsf_subsystem_name",expect_type=Input).value = self.base_traits.subsystem_name

        if self.base_traits.subsystem_userid is not None:
            self.get_child_by_id(id="rrsf_subsystem_userid",expect_type=Input).value = self.base_traits.subsystem_userid

    def compose(self) -> ComposeResult:
        yield Label("Subsystem name: ", classes="rrsf-label")
        yield Input(id="rrsf_subsystem_name", max_length=8, disabled=True, compact=True, classes="rrsf-metadata")
        
        yield Label("Subsystem userid: ", classes="rrsf-label")
        yield Input(id="rrsf_subsystem_userid", max_length=8, disabled=True, compact=True, classes="rrsf-metadata")

class PanelRRSF(VerticalScroll):
    base_traits: reactive[BaseRRSFTraits] = reactive(BaseRRSFTraits())

    def on_mount(self) -> None:
        rrsf_options = get_rrsf_options()
        self.get_child_by_type(PanelRRSFNodes).base_traits = BaseRRSFTraits.from_dict(prefix="base",source=rrsf_options["profile"]["base"])
        self.get_child_by_type(PanelRRSFMetaData).base_traits = BaseRRSFTraits.from_dict(prefix="base",source=rrsf_options["profile"]["base"])

    def compose(self) -> ComposeResult:
        yield PanelRRSFMetaData()
        yield PanelRRSFNodes()