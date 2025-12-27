
from collections.abc import Generator

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import VerticalGroup, HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from textual.suggester import SuggestFromList
from textual.widgets import Button, ContentSwitcher, DataTable, Input, Label, Select

from blackwall.api.rrsf import (
    BaseRRSFTraits,
    get_rrsf_options,
)
from blackwall.panels.traits_ui import generate_trait_inputs


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

    def compose(self) -> ComposeResult:
        if self.base_traits.subsystem_name is not None:
            yield Label(f"Subsystem name: {self.base_traits.subsystem_name}")
        
        if self.base_traits.subsystem_userid is not None:
            yield Label(f"Subsystem userid: {self.base_traits.subsystem_userid}")

class PanelRRSF(VerticalScroll):
    base_traits: reactive[BaseRRSFTraits] = reactive(BaseRRSFTraits())

    def on_mount(self) -> None:
        rrsf_options = get_rrsf_options()
        self.notify(rrsf_options["subystem_name"])
        self.get_child_by_type(PanelRRSFNodes).base_traits = BaseRRSFTraits.from_dict(prefix="base",source=rrsf_options["profile"]["base"])
        self.get_child_by_type(PanelRRSFMetaData).base_traits = BaseRRSFTraits.from_dict(prefix="base",source=rrsf_options["profile"]["base"])

    def compose(self) -> ComposeResult:
        yield PanelRRSFMetaData()
        yield PanelRRSFNodes()