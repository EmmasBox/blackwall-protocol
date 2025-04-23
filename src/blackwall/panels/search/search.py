
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

                user_dict = user.get_user(username=search_query)


                
            
                base_traits = user.BaseUserTraits.from_dict(prefix="base",source=user_dict["profile"]["base"])

                new_user_panel.user_info = UserInfo(
                    base_traits=base_traits,
                    username=search_query,
                    mode=PanelMode.edit
                )

                if "tso" in user_dict:
                    new_user_panel.tso_traits = user.TSOUserTraits.from_dict(prefix="tso",source=user_dict["profile"]["tso"])

                if "omvs" in user_dict:
                    new_user_panel.omvs_traits = user.OMVSUserTraits.from_dict(prefix="omvs",source=user_dict["profile"]["omvs"])

                if "nds" in user_dict:
                    new_user_panel.nds_traits = user.NDSUserTraits.from_dict(prefix="nds",source=user_dict["profile"]["nds"])

                if "cics" in user_dict:
                    new_user_panel.cics_traits = user.CICSUserTraits.from_dict(prefix="cics",source=user_dict["profile"]["cics"])

                if "netview" in user_dict:
                    new_user_panel.netview_traits = user.NetviewUserTraits.from_dict(prefix="netview",source=user_dict["profile"]["netview"])

                if "mfa" in user_dict:
                    new_user_panel.mfa_traits = user.MfaUserTraits.from_dict(prefix="mfa",source=user_dict["profile"]["mfa"])
                
                if "eim" in user_dict:
                    new_user_panel.eim_traits = user.EIMUserTraits.from_dict(prefix="eim",source=user_dict["profile"]["eim"])

                if "workattr" in user_dict:
                    new_user_panel.workattr_traits = user.WorkattrUserTraits.from_dict(prefix="workattr",source=user_dict["profile"]["workattr"])
                
                if "ovm" in user_dict:
                    new_user_panel.ovm_traits = user.OvmUserTraits.from_dict(prefix="ovm",source=user_dict["profile"]["ovm"])

                if "dce" in user_dict:
                    new_user_panel.dce_traits = user.DCEUserTraits.from_dict(prefix="dce",source=user_dict["profile"]["dce"])
                
                if "dfp" in user_dict:
                    new_user_panel.dfp_traits = user.DFPUserTraits.from_dict(prefix="dfp",source=user_dict["profile"]["dfp"])

                if "operparm" in user_dict:
                    new_user_panel.operparm_traits = user.OperparmUserTraits.from_dict(prefix="operparm",source=user_dict["profile"]["operparm"])

                if "proxy" in user_dict:
                    new_user_panel.proxy_traits = user.ProxyUserTraits.from_dict(prefix="proxy",source=user_dict["profile"]["proxy"])
                
                if "lnotes" in user_dict:
                    new_user_panel.lnotes_traits = user.LnotesUserTraits.from_dict(prefix="lnotes",source=user_dict["profile"]["lnotes"])

                if "language" in user_dict:
                    new_user_panel.lang_traits = user.LanguageUserTraits.from_dict(prefix="language",source=user_dict["profile"]["language"])

                if "kerb" in user_dict:
                    new_user_panel.kerb_traits = user.KerbUserTraits.from_dict(prefix="kerb",source=user_dict["profile"]["kerb"])
                
                self.post_message(OpenTab(f"User: {search_query}",new_user_panel))

                self.notify(f"Found user: {search_query}")
        elif search_type == "search_type_group":
            pass
        elif search_type == "search_type_dataset":
            pass
        elif search_type == "search_type_resource":
            pass
