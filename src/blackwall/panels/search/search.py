
#TODO fix all of this shitty code. Not gonna lie the code below is really bad, but I was in a crunch

from textual import on
from textual.app import ComposeResult
from textual.widgets import Button, Input, Label, RadioButton, RadioSet
from textual.containers import HorizontalGroup, VerticalScroll

from blackwall.messages import OpenTab
from blackwall.panels.panel_mode import PanelMode
from blackwall.panels.search.results import PanelResultsMixedType
from blackwall.panels.users.user import PanelUser, UserInfo

from blackwall.panels.search.search_backend import search_database_query_one, QueryType

from blackwall.api import user

class SearchSelector(HorizontalGroup):
    def compose(self) -> ComposeResult:
        with RadioSet(id="type_selector",classes="search-selector"):
            yield RadioButton("Any",id="search_type_any",value=False,disabled=True)
            yield RadioButton("User",id="search_type_user",value=True)
            yield RadioButton("Group",id="search_type_group")
            yield RadioButton("Dataset profile",id="search_type_dataset")
            yield RadioButton("Resource profile",id="search_type_resource")
        with RadioSet(id="filter-selector",classes="search-selector"):
            yield RadioButton("All",disabled=True)
            yield RadioButton("Only one",value=True)

class SearchField(HorizontalGroup):
    def __init__(self, search_action: str):
        super().__init__()
        self.search_action = search_action

    def compose(self) -> ComposeResult:
        yield Label("Search:")
        yield Input(name="Search",id="search_field",classes="search-field")
        yield Button("Search",action="search")

    def on_mount(self) -> None:
        search_field = self.get_child_by_id("search_field",Input)
        search_field.focus()

    async def action_search(self):
        await self.app.run_action(self.search_action,default_namespace=self.parent)

class PanelSearch(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield SearchSelector()
        yield SearchField(search_action="search")

    @on(Input.Submitted)
    def action_search(self) -> None:
        search_query = self.get_child_by_type(SearchField).get_child_by_id("search_field",Input).value
        search_type = self.get_child_by_type(SearchSelector).get_child_by_id("type_selector",RadioSet).pressed_button.id
        if search_type == "search_type_any":
            results = search_database_query_one(query=search_query, class_name=None,query_types=QueryType.all())
            self.post_message(OpenTab("Results",PanelResultsMixedType(results)))
        elif search_type == "search_type_user":
            if user.user_exists(username=search_query):
                new_user_panel = PanelUser()

                new_user_panel.user_info = UserInfo(
                    username=search_query,
                    mode=PanelMode.edit
                )
                self.post_message(OpenTab(f"User: {search_query}",new_user_panel))

                self.notify(f"Found user: {search_query}")
        elif search_type == "search_type_group":
            pass
        elif search_type == "search_type_dataset":
            pass
        elif search_type == "search_type_resource":
            pass
