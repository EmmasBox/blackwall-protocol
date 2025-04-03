
from textual.app import ComposeResult
from textual.widgets import Label, DataTable
from textual.containers import VerticalGroup, VerticalScroll

USER_COLUMNS = [
    ("User", "Owner", "dfltgrp", "SOA", "RIRP", "UID", "Shell", "Home", "Last logon", "Created"),
]

DATASET_COLUMNS = [
    ("Dataset", "UACC", "Owner", "Created"),
]

class PanelResultsMixedType(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Label("Users:")
        yield DataTable(id="results_user_table")
        yield Label("Groups:")
        yield DataTable(id="results_group_table")
        yield Label("Dataset profiles:")
        yield DataTable(id="results_dataset_table")
        yield Label("General resources profiles:")
        yield DataTable(id="results_resource_table")

class PanelResultsSingleType(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield DataTable()

class PanelResultUser(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield DataTable()        

class PanelResultDataset(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield DataTable()        