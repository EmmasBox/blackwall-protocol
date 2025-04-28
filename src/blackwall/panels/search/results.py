
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import DataTable, Label

from blackwall.panels.search.search_backend import QueryType

USER_COLUMNS = [
    ("User", "Owner", "dfltgrp", "SOA", "RIRP", "UID", "Shell", "Home", "Last logon", "Created"),
]

GROUP_COLUMNS = [
    ("Group", "Connected users", "Created"),
]

DATASET_COLUMNS = [
    ("Dataset", "UACC", "Owner", "Created"),
]

class PanelResultsUsers(VerticalScroll):
    def __init__(self, user_dict: dict):
        super().__init__()
        self.user_dict = user_dict

    def compose(self) -> ComposeResult:
        yield Label("Users:")
        yield DataTable(id="results_user_table")     

    def on_mount(self) -> None:
        user_table = self.get_child_by_id("results_user_table",DataTable)
        user_table.zebra_stripes = True
        user_table.add_columns(*USER_COLUMNS[0]) 

class PanelResultsGroup(VerticalScroll):
    def __init__(self, group_dict: dict):
        super().__init__()
        self.group_dict = group_dict

    def compose(self) -> ComposeResult:
        yield Label("Groups:")
        yield DataTable(id="results_group_table")    

    def on_mount(self) -> None:
        group_table = self.get_child_by_id("results_group_table",DataTable)
        group_table.zebra_stripes = True
        group_table.add_columns(*GROUP_COLUMNS[0])

class PanelResultsDatasets(VerticalScroll):
    def __init__(self, dataset_dict: dict):
        super().__init__()
        self.dataset_dict = dataset_dict

    def compose(self) -> ComposeResult:
        yield Label("Dataset profiles:")
        yield DataTable(id="results_dataset_table")        

    def on_mount(self) -> None:
        dataset_table = self.get_child_by_id("results_dataset_table",DataTable)
        dataset_table.zebra_stripes = True
        dataset_table.add_columns(*DATASET_COLUMNS[0])

class PanelResultsResources(VerticalScroll):
    def __init__(self, resource_dict: dict):
        super().__init__()
        self.resource_dict = resource_dict

    def compose(self) -> ComposeResult:
        yield Label("General resources profiles:")
        yield DataTable(id="results_dataset_table")        

class PanelResultsMixedType(VerticalScroll):
    def __init__(self, results: dict[QueryType,dict]):
        super().__init__()
        self.results = results

    def compose(self) -> ComposeResult:
        if QueryType.User in self.results:
            yield PanelResultsUsers(user_dict=self.results[QueryType.User])
        if QueryType.Group in self.results:
            yield PanelResultsGroup(group_dict=self.results[QueryType.Group])
        if QueryType.Dataset in self.results:
            yield PanelResultsDatasets(dataset_dict=self.results[QueryType.Dataset])
        if QueryType.Resource in self.results:
            yield PanelResultsResources(resource_dict=self.results[QueryType.Resource])