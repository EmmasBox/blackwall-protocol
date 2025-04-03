
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

class PanelResultsUsers(VerticalScroll):
    def __init__(self, user_dict: dict):
        super().__init__()
        self.user_dict = user_dict

    def compose(self) -> ComposeResult:
        yield Label("Users:")
        yield DataTable(id="results_user_table")     

    def on_mount(self) -> None:
        user_table = self.query_exactly_one(selector="#results_user_table")
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
        group_table = self.query_exactly_one(selector="#results_group_table")
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
        dataset_table = self.query_exactly_one(selector="#results_dataset_table")
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
    def __init__(self, user_dict: dict, group_dict: dict, dataset_dict: dict, resource_dict: dict):
        super().__init__()
        self.user_dict = user_dict
        self.group_dict = group_dict
        self.dataset_dict = dataset_dict
        self.resource_dict = resource_dict

    def compose(self) -> ComposeResult:
        yield PanelResultsUsers(user_dict=self.user_dict)
        yield PanelResultsGroup(group_dict=self.group_dict)
        yield PanelResultsDatasets(dataset_dict=self.dataset_dict)
        yield PanelResultsResources(resource_dict=self.resource_dict)