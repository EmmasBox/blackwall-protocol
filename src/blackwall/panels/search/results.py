
from textual.app import ComposeResult
from textual.widgets import Label, DataTable
from textual.containers import VerticalGroup, VerticalScroll

USER_COLUMNS = [
    ("User", "Owner", "dfltgrp", "SOA", "RIRP", "UID", "Shell", "Home", "Last logon", "Created"),
]

GROUP_COLUMNS = [
    ("Group", "Connected users", "Created"),
]

DATASET_COLUMNS = [
    ("Dataset", "UACC", "Owner", "Created"),
]

class PanelResultsMixedType(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("Users:")
        yield DataTable(id="results_user_table",)
        yield Label("Groups:")
        yield DataTable(id="results_group_table")
        yield Label("Dataset profiles:")
        yield DataTable(id="results_dataset_table")
        yield Label("General resources profiles:")
        yield DataTable(id="results_resource_table")

    def on_mount(self) -> None:
        user_table = self.query_exactly_one(selector="#results_user_table")
        user_table.zebra_stripes = True
        user_table.add_columns(*USER_COLUMNS[0])

        group_table = self.query_exactly_one(selector="#results_group_table")
        group_table.zebra_stripes = True
        group_table.add_columns(*GROUP_COLUMNS[0])

        dataset_table = self.query_exactly_one(selector="#results_dataset_table")
        dataset_table.zebra_stripes = True
        dataset_table.add_columns(*DATASET_COLUMNS[0])

class PanelResultsSingleType(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield DataTable()

class PanelResultUser(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield DataTable()        

class PanelResultDataset(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield DataTable()        