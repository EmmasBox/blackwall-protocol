
from collections.abc import Generator

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.reactive import reactive
from textual.suggester import SuggestFromList
from textual.widgets import Button, ContentSwitcher, DataTable, Input, Label, Select

from blackwall.api.rrsf import (
    BaseRRSFTraits,
    get_rrsf_options,
)


def generate_rrsf_node(node: dict) -> Generator:
    if "node_name" in node:
        yield Label(node["node_name"])

    if "multisystem_node_name" in node:
        yield Label(f"System: {node["multisystem_node_name"]}")

class PanelRRSFNodes(VerticalGroup):
    base_traits: reactive[BaseRRSFTraits] = reactive(BaseRRSFTraits())

    def compose(self) -> ComposeResult:
        if self.base_traits.nodes is not None:
            for node in self.base_traits.nodes:
                yield from generate_rrsf_node(node)

class PanelRRSFMetaData(HorizontalGroup):
    base_traits: reactive[BaseRRSFTraits] = reactive(BaseRRSFTraits())

    def on_mount(self) -> None:
        if self.base_traits.subsystem_name is not None:
            self.notify(self.base_traits.subsystem_name)

    def watch_base_traits(self):
        pass

    def compose(self) -> ComposeResult:
        yield Label("Subsystem name: ")
        yield Input(id="rrsf_subsystem_name", max_length=8, disabled=True, compact=True,classes="field-short-generic")
        
        yield Label("Subsystem userid: ")
        yield Input(id="rrsf_subsystem_userid", max_length=8, disabled=True, compact=True,classes="field-short-generic")

class PanelRRSF(VerticalScroll):
    base_traits: reactive[BaseRRSFTraits] = reactive(BaseRRSFTraits())

    def on_mount(self) -> None:
        rrsf_options = get_rrsf_options()
        self.get_child_by_type(PanelRRSFNodes).base_traits = BaseRRSFTraits.from_dict(prefix="base",source=rrsf_options["profile"]["base"])
        self.get_child_by_type(PanelRRSFMetaData).base_traits = BaseRRSFTraits.from_dict(prefix="base",source=rrsf_options["profile"]["base"])

    def compose(self) -> ComposeResult:
        yield PanelRRSFMetaData()
        yield PanelRRSFNodes()