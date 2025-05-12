
#TODO fix all of this shitty code. Not gonna lie the code below is really bad, but I was in a crunch

from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.suggester import SuggestFromList
from textual.widgets import Button, ContentSwitcher, Input, Label

from blackwall.api import dataset, group, keyrings, resource, user
from blackwall.api.setropts import get_active_classes
from blackwall.emoji import get_emoji
from blackwall.messages import OpenTab
from blackwall.panels.dataset.dataset import DatasetInfo, PanelDataset
from blackwall.panels.group.group import GroupInfo, PanelGroup
from blackwall.panels.keyrings.keyrings import KeyringInfo, PanelKeyring
from blackwall.panels.panel_mode import PanelMode
from blackwall.panels.resource.resource import PanelResource, ResourceInfo
from blackwall.panels.search.results import PanelResultsMixedType
from blackwall.panels.search.search_backend import QueryType, search_database_query_one
from blackwall.panels.users.user import PanelUser, UserInfo
from blackwall.regex import racf_id_regex


class PanelSearchUser(VerticalGroup):
    def __init__(self, search_action: str, id: str):  # noqa: A002
        super().__init__()
        self.id = id
        self.search_action = search_action

    def compose(self) -> ComposeResult:
        yield Label("Search users",classes="search-label")
        yield Input(max_length=8,placeholder="id...",restrict=racf_id_regex,id="search_field",classes="field-short-generic")
        yield Button(label=f"{get_emoji("🔎")} Search",action="search")

    async def action_search(self):
        await self.app.run_action(self.search_action,default_namespace=self.parent)

class PanelSearchGroup(VerticalGroup):
    def __init__(self, search_action: str, id: str):  # noqa: A002
        super().__init__()
        self.id = id
        self.search_action = search_action

    def compose(self) -> ComposeResult:
        yield Label("Search for group",classes="search-label")
        yield Input(max_length=8,placeholder="id...",id="search_field",restrict=racf_id_regex,classes="field-short-generic")
        yield Button(label=f"{get_emoji("🔎")} Search",action="search")

    async def action_search(self):
        await self.app.run_action(self.search_action,default_namespace=self.parent)

class PanelSearchDataset(VerticalGroup):
    def __init__(self, search_action: str, id: str):  # noqa: A002
        super().__init__()
        self.id = id
        self.search_action = search_action

    def compose(self) -> ComposeResult:
        yield Label("Search for dataset profile",classes="search-label")
        yield Input(max_length=255,placeholder="dataset profile name...",id="search_field",classes="field-long-generic")
        yield Button(label=f"{get_emoji("🔎")} Search",action="search")

    async def action_search(self):
        await self.app.run_action(self.search_action,default_namespace=self.parent)

class PanelSearchResource(VerticalGroup):
    def __init__(self, search_action: str, id: str):  # noqa: A002
        super().__init__()
        self.id = id
        self.search_action = search_action

    active_classes = get_active_classes()

    def compose(self) -> ComposeResult:
        yield Label("Search for resource profile",classes="search-label")
        yield Input(max_length=8,id="search_field_class",suggester=SuggestFromList(self.active_classes,case_sensitive=False),placeholder="class...",classes="field-short-generic")
        yield Input(max_length=255,placeholder="resource profile...",classes="field-long-generic")
        yield Button(label=f"{get_emoji("🔎")} Search",action="search")

    async def action_search(self):
        await self.app.run_action(self.search_action,default_namespace=self.parent)

class PanelSearchSwitcherButtons(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Button(id="search_user_panel_button",label="User",classes="search-buttons",name="search_user_panel")
        yield Button(id="search_group_panel_button",label="Group",classes="search-buttons",name="search_group_panel")
        yield Button(id="search_dataset_panel_button",label="Dataset profile",classes="search-buttons",name="search_dataset_panel")
        yield Button(id="search_resource_panel_button",label="Resource profile",classes="search-buttons",name="search_resource_panel")
        #yield Button(id="search_keyring_panel",label="Keyring",classes="search-buttons")

class PanelSearch(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelSearchSwitcherButtons()
        with ContentSwitcher(initial="search_user_panel",id="search_switcher",classes="search-switcher"):
            yield PanelSearchUser(search_action="search",id="search_user_panel")
            yield PanelSearchGroup(search_action="search",id="search_group_panel")
            yield PanelSearchDataset(search_action="search",id="search_dataset_panel")
            yield PanelSearchResource(search_action="search",id="search_resource_panel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.name  

    @on(Input.Submitted)
    def action_search(self) -> None:
        search_switcher_id = self.query_exactly_one("#search_switcher", ContentSwitcher).current
        if search_switcher_id is not None:
            search_query = self.query_exactly_one(f"#{search_switcher_id}").query_exactly_one("#search_field",Input).value
        
            if search_switcher_id == "search_any_panel":
                results = search_database_query_one(query=search_query, class_name=None,query_types=QueryType.all())
                self.post_message(OpenTab("Results",PanelResultsMixedType(results)))
            elif search_switcher_id == "search_user_panel":
                if user.user_exists(username=search_query):
                    new_user_panel = PanelUser()

                    user_dict = user.get_user(username=search_query)
                
                    base_traits = user.BaseUserTraits.from_dict(prefix="base",source=user_dict["profile"]["base"])

                    new_user_panel.user_info = UserInfo(
                        base_traits=base_traits,
                        username=search_query,
                        mode=PanelMode.edit,
                    )

                    if 'profile' in user_dict and 'tso' in user_dict['profile']:
                        new_user_panel.user_info.tso_traits = user.TSOUserTraits.from_dict(prefix="tso",source=user_dict["profile"]["tso"])

                    if 'profile' in user_dict and 'omvs' in user_dict['profile']:
                        new_user_panel.user_info.omvs_traits = user.OMVSUserTraits.from_dict(prefix="omvs",source=user_dict["profile"]["omvs"])

                    if 'profile' in user_dict and 'nds' in user_dict['profile']:
                        new_user_panel.user_info.nds_traits = user.NDSUserTraits.from_dict(prefix="nds",source=user_dict["profile"]["nds"])

                    if 'profile' in user_dict and 'cics' in user_dict['profile']:
                        new_user_panel.user_info.cics_traits = user.CICSUserTraits.from_dict(prefix="cics",source=user_dict["profile"]["cics"])

                    if 'profile' in user_dict and 'netview' in user_dict['profile']:
                        new_user_panel.user_info.netview_traits = user.NetviewUserTraits.from_dict(prefix="netview",source=user_dict["profile"]["netview"])

                    if 'profile' in user_dict and 'mfa' in user_dict['profile']:
                        new_user_panel.user_info.mfa_traits = user.MfaUserTraits.from_dict(prefix="mfa",source=user_dict["profile"]["mfa"])
                    
                    if 'profile' in user_dict and 'eim' in user_dict['profile']:
                        new_user_panel.user_info.eim_traits = user.EIMUserTraits.from_dict(prefix="eim",source=user_dict["profile"]["eim"])

                    if 'profile' in user_dict and 'workattr' in user_dict['profile']:
                        new_user_panel.user_info.workattr_traits = user.WorkattrUserTraits.from_dict(prefix="workattr",source=user_dict["profile"]["workattr"])
                    
                    if 'profile' in user_dict and 'ovm' in user_dict['profile']:
                        new_user_panel.user_info.ovm_traits = user.OvmUserTraits.from_dict(prefix="ovm",source=user_dict["profile"]["ovm"])

                    if 'profile' in user_dict and 'dce' in user_dict['profile']:
                        new_user_panel.user_info.dce_traits = user.DCEUserTraits.from_dict(prefix="dce",source=user_dict["profile"]["dce"])
                    
                    if 'profile' in user_dict and 'dfp' in user_dict['profile']:
                        new_user_panel.user_info.dfp_traits = user.DFPUserTraits.from_dict(prefix="dfp",source=user_dict["profile"]["dfp"])

                    if 'profile' in user_dict and 'operparm' in user_dict['profile']:
                        new_user_panel.user_info.operparm_traits = user.OperparmUserTraits.from_dict(prefix="operparm",source=user_dict["profile"]["operparm"])

                    if 'profile' in user_dict and 'proxy' in user_dict['profile']:
                        new_user_panel.user_info.proxy_traits = user.ProxyUserTraits.from_dict(prefix="proxy",source=user_dict["profile"]["proxy"])
                    
                    if 'profile' in user_dict and 'lnotes' in user_dict['profile']:
                        new_user_panel.user_info.lnotes_traits = user.LnotesUserTraits.from_dict(prefix="lnotes",source=user_dict["profile"]["lnotes"])

                    if 'profile' in user_dict and 'language' in user_dict['profile']:
                        new_user_panel.user_info.lang_traits = user.LanguageUserTraits.from_dict(prefix="language",source=user_dict["profile"]["language"])

                    if 'profile' in user_dict and 'kerb' in user_dict['profile']:
                        new_user_panel.user_info.kerb_traits = user.KerbUserTraits.from_dict(prefix="kerb",source=user_dict["profile"]["kerb"])
                    
                    self.post_message(OpenTab(f"User: {search_query}",new_user_panel))

                    self.notify(f"Found user: {search_query}")
                else:
                    self.notify(f"User {search_query} couldn't be found")
            elif search_switcher_id == "search_group_panel":
                if group.group_exists(group=search_query):
                    new_group_panel = PanelGroup()

                    group_dict = group.get_group(group=search_query)
                
                    base_traits = group.BaseGroupTraits.from_dict(prefix="base",source=group_dict["profile"]["base"])

                    new_group_panel.group_info = GroupInfo(
                        base_traits=base_traits,
                        group_name=search_query,
                    )

                    if 'profile' in group_dict and 'dfp' in group_dict['profile']:
                        new_group_panel.group_info.dfp_traits = group.DFPGroupTraits.from_dict(prefix="dfp",source=group_dict["profile"]["dfp"])

                    self.post_message(OpenTab(f"Group: {search_query}",new_group_panel))

                    self.notify(f"Found group: {search_query}")
                else:
                    self.notify(f"Group {search_query} couldn't be found")
            elif search_switcher_id == "search_dataset_panel":
                if dataset.dataset_profile_exists(dataset=search_query):
                    new_dataset_panel = PanelDataset()

                    dataset_dict = dataset.get_dataset_profile(dataset=search_query)
                
                    base_traits = dataset.BaseDatasetTraits.from_dict(prefix="base",source=dataset_dict["profile"]["base"])

                    new_dataset_panel.dataset_info = DatasetInfo(
                        base_traits=base_traits,
                        profile_name=search_query,
                    )

                    self.post_message(OpenTab(f"Dataset: {search_query}",new_dataset_panel))

                    self.notify(f"Found dataset profile: {search_query}")
                else:
                    self.notify(f"Dataset profile {search_query} couldn't be found")
            elif search_switcher_id == "search_resource_panel":
                search_query_class = self.query_exactly_one(f"#{search_switcher_id}").query_exactly_one("#search_field_class",Input).value

                if resource.resource_profile_exists(resource=search_query,resource_class=search_query_class):
                    new_resource_panel = PanelResource()

                    resource_dict = resource.get_resource_profile(resource=search_query,resource_class=search_query_class)
                
                    base_traits = resource.BaseResourceTraits.from_dict(prefix="base",source=resource_dict["profile"]["base"])

                    new_resource_panel.resource_info = ResourceInfo(
                        base_traits=base_traits,
                        resource_class=search_query_class,
                        resource_name=search_query,
                    )

                    if 'profile' in resource_dict and 'kerb' in resource_dict['profile']:
                        new_resource_panel.resource_info.kerb_traits = resource.KerbResourceTraits.from_dict(prefix="kerb",source=resource_dict["profile"]["kerb"])

                    if 'profile' in resource_dict and 'dlf' in resource_dict['profile']:
                        new_resource_panel.resource_info.dlf_traits = resource.DLFDataResourceTraits.from_dict(prefix="dlf",source=resource_dict["profile"]["dlf"])

                    if 'profile' in resource_dict and 'eim' in resource_dict['profile']:
                        new_resource_panel.resource_info.eim_traits = resource.EIMResourceTraits.from_dict(prefix="eim",source=resource_dict["profile"]["eim"])

                    if 'profile' in resource_dict and 'jes' in resource_dict['profile']:
                        new_resource_panel.resource_info.jes_traits = resource.JESResourceTraits.from_dict(prefix="jes",source=resource_dict["profile"]["jes"])

                    if 'profile' in resource_dict and 'icsf' in resource_dict['profile']:
                        new_resource_panel.resource_info.icsf_traits = resource.ICSFResourceTraits.from_dict(prefix="icsf",source=resource_dict["profile"]["icsf"])

                    if 'profile' in resource_dict and 'kerb' in resource_dict['profile']:
                        new_resource_panel.resource_info.kerb_traits = resource.KerbResourceTraits.from_dict(prefix="kerb",source=resource_dict["profile"]["kerb"])

                    if 'profile' in resource_dict and 'ictx' in resource_dict['profile']:
                        new_resource_panel.resource_info.ictx_traits = resource.ICTXResourceTraits.from_dict(prefix="ictx",source=resource_dict["profile"]["ictx"])

                    if 'profile' in resource_dict and 'idtparms' in resource_dict['profile']:
                        new_resource_panel.resource_info.idtparms_traits = resource.IDTPARMSResourceTraits.from_dict(prefix="idtparms",source=resource_dict["profile"]["idtparms"])

                    if 'profile' in resource_dict and 'session' in resource_dict['profile']:
                        new_resource_panel.resource_info.session_traits = resource.SessionResourceTraits.from_dict(prefix="session",source=resource_dict["profile"]["session"])

                    if 'profile' in resource_dict and 'svfmr' in resource_dict['profile']:
                        new_resource_panel.resource_info.svfmr_traits = resource.SVFMRResourceTraits.from_dict(prefix="svfmr",source=resource_dict["profile"]["svfmr"])

                    if 'profile' in resource_dict and 'stdata' in resource_dict['profile']:
                        new_resource_panel.resource_info.stdata_traits = resource.STDATAResourceTraits.from_dict(prefix="stdata",source=resource_dict["profile"]["stdata"])

                    if 'profile' in resource_dict and 'proxy' in resource_dict['profile']:
                        new_resource_panel.resource_info.proxy_traits = resource.ProxyResourceTraits.from_dict(prefix="proxy",source=resource_dict["profile"]["proxy"])

                    if 'profile' in resource_dict and 'mfpolicy' in resource_dict['profile']:
                        new_resource_panel.resource_info.mfpolicy_traits = resource.MFPolicyResourceTraits.from_dict(prefix="mfpolicy",source=resource_dict["profile"]["mfpolicy"])

                    if 'profile' in resource_dict and 'sigver' in resource_dict['profile']:
                        new_resource_panel.resource_info.sigver_traits = resource.SIGVERResourceTraits.from_dict(prefix="sigver",source=resource_dict["profile"]["sigver"])

                    if 'profile' in resource_dict and 'tme' in resource_dict['profile']:
                        new_resource_panel.resource_info.tme_traits = resource.TMEResourceTraits.from_dict(prefix="tme",source=resource_dict["profile"]["tme"])

                    if 'profile' in resource_dict and 'cdtinfo' in resource_dict['profile']:
                        new_resource_panel.resource_info.cdtinfo_traits = resource.CDTINFOResourceTraits.from_dict(prefix="cdtinfo",source=resource_dict["profile"]["cdtinfo"])

                    if 'profile' in resource_dict and 'ssignon' in resource_dict['profile']:
                        new_resource_panel.resource_info.ssignon_traits = resource.SSIGNONResourceTraits.from_dict(prefix="ssignon",source=resource_dict["profile"]["ssignon"])

                    if 'profile' in resource_dict and 'cfdef' in resource_dict['profile']:
                        new_resource_panel.resource_info.cfdef_traits = resource.CfdefResourceTraits.from_dict(prefix="cfdef",source=resource_dict["profile"]["cfdef"])

                    self.post_message(OpenTab(f"Resource: {search_query}",new_resource_panel))

                    self.notify(f"Found resource profile: {search_query}")
                else:
                    self.notify(f"Resource profile {search_query} couldn't be found")
            elif search_switcher_id == "search_keyring_panel":
                search_query_keyring_owner = self.query_exactly_one(f"#{search_switcher_id}").query_exactly_one("#search_field_keyring_owner",Input).value

                if keyrings.keyring_exists(keyring=search_query,owner=search_query_keyring_owner):
                    new_keyring_panel = PanelKeyring()

                    key_dict = keyrings.get_keyring(keyring=search_query,owner=search_query_keyring_owner)

                    keyring_traits = keyrings.KeyringTraits.from_dict(prefix=None,source=key_dict)

                    new_keyring_panel.keyring_info = KeyringInfo(
                        keyring_name=search_query,
                        keyring_owner=search_query_keyring_owner,
                        keyring_traits=keyring_traits,
                    )

                    self.post_message(OpenTab(f"Keyring: {search_query}",new_keyring_panel))

                    self.notify(f"Found keyring: {search_query}")
                else:
                    self.notify(f"Keyring {search_query} couldn't be found")
