
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import DataTable, Input, Label

from blackwall.api.rrsf import (
    BaseRRSFTraits,
    get_rrsf_options,
)
from blackwall.emoji import get_emoji

RRSF_COLUMNS = [
    (
     "Node", 
     "System", 
     "Description", 
     "State", 
     "Protocol",
     f"Requests denied{get_emoji(" ❌")}" , 
     f"Received work{get_emoji(" 🔻")}" , 
     f"Sent work{get_emoji(" 🔺")}" , 
     ),
]

def rrsf_get_key(key: str, dict: dict) -> str:
    if key in dict:
        return str(dict[key])
    else:
        return ""

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
                    rrsf_get_key("base:node_name", node),
                    rrsf_get_key("base:multisystem_node_name", node),
                    rrsf_get_key("base:node_description", node),
                    rrsf_get_key("base:node_state", node),
                    rrsf_get_key("base:node_protocol", node).upper(),
                    rrsf_get_key("base:requests_denied", node),
                    f"{rrsf_get_key("base:time_of_last_received_work", node)} {rrsf_get_key("base:date_of_last_received_work", node)}",
                    f"{rrsf_get_key("base:time_of_last_sent_work", node)} {rrsf_get_key("base:date_of_last_sent_work", node)}",
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
        
        if self.base_traits.subsystem_operator_prefix is not None:
            self.get_child_by_id(id="rrsf_subsystem_operator_prefix",expect_type=Input).value = self.base_traits.subsystem_operator_prefix

    def compose(self) -> ComposeResult:
        yield Label("Subsystem name: ", classes="rrsf-label")
        yield Input(id="rrsf_subsystem_name", max_length=8, disabled=True, compact=True, classes="rrsf-metadata")
        
        yield Label("Subsystem userid: ", classes="rrsf-label")
        yield Input(id="rrsf_subsystem_userid", max_length=8, disabled=True, compact=True, classes="rrsf-metadata")

        yield Label("Operator prefix: ", classes="rrsf-label")
        yield Input(id="rrsf_subsystem_operator_prefix", max_length=8, disabled=True, compact=True, classes="rrsf-metadata")

class PanelRRSF(VerticalScroll):
    base_traits: reactive[BaseRRSFTraits] = reactive(BaseRRSFTraits())

    def on_mount(self) -> None:
        rrsf_options = get_rrsf_options()
        self.get_child_by_type(PanelRRSFNodes).base_traits = BaseRRSFTraits.from_dict(prefix="base",source=rrsf_options["profile"]["base"])
        self.get_child_by_type(PanelRRSFMetaData).base_traits = BaseRRSFTraits.from_dict(prefix="base",source=rrsf_options["profile"]["base"])

    def compose(self) -> ComposeResult:
        yield PanelRRSFMetaData()
        yield PanelRRSFNodes()