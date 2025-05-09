
#TODO fix all of this shitty code. Not gonna lie the code below is really bad, but I was in a crunch

from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Button, Input, Label, RadioButton, RadioSet

from blackwall.api import dataset, group, keyrings, resource, user
from blackwall.messages import OpenTab
from blackwall.panels.dataset.dataset import DatasetInfo, PanelDataset
from blackwall.panels.group.group import GroupInfo, PanelGroup
from blackwall.panels.keyrings.keyrings import KeyringInfo, PanelKeyring
from blackwall.panels.panel_mode import PanelMode
from blackwall.panels.resource.resource import PanelResource, ResourceInfo
from blackwall.panels.search.results import PanelResultsMixedType
from blackwall.panels.search.search_backend import QueryType, search_database_query_one
from blackwall.panels.users.user import PanelUser, UserInfo


class SearchSelector(HorizontalGroup):
    def compose(self) -> ComposeResult:
        with RadioSet(id="type_selector",classes="search-selector"):
            yield RadioButton("Any",id="search_type_any",value=False,disabled=True)
            yield RadioButton("User",id="search_type_user",value=True)
            yield RadioButton("Group",id="search_type_group")
            yield RadioButton("Dataset profile",id="search_type_dataset")
            yield RadioButton("Resource profile",id="search_type_resource")
            #yield RadioButton("Keyring",id="search_type_keyring")
        with RadioSet(id="filter-selector",classes="search-selector"):
            yield RadioButton("All",disabled=True)
            yield RadioButton("Only one",value=True)

class SearchField(HorizontalGroup):
    def __init__(self, search_action: str):
        super().__init__()
        self.search_action = search_action

    def compose(self) -> ComposeResult:
        yield Label("Search:")
        yield Input(name="Class",max_length=8,id="search_field_class",classes="field-short-generic")
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
        search_query_class = self.get_child_by_type(SearchField).get_child_by_id("search_field_class",Input).value
        search_type = self.get_child_by_type(SearchSelector).get_child_by_id("type_selector",RadioSet).pressed_button.id # type: ignore
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
        elif search_type == "search_type_group":
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
        elif search_type == "search_type_dataset":
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
        elif search_type == "search_type_resource":
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
        elif search_type == "search_type_keyring":
            if keyrings.keyring_exists(keyring=search_query,owner=search_query_class):
                new_keyring_panel = PanelKeyring()

                key_dict = keyrings.get_keyring(keyring=search_query,owner=search_query_class)

                keyring_traits = keyrings.KeyringTraits.from_dict(prefix=None,source=key_dict)

                new_keyring_panel.keyring_info = KeyringInfo(
                    keyring_name=search_query,
                    keyring_owner=search_query_class,
                    keyring_traits=keyring_traits,
                )

                self.post_message(OpenTab(f"Keyring: {search_query}",new_keyring_panel))

                self.notify(f"Found keyring: {search_query}")
            else:
                self.notify(f"Keyring {search_query} couldn't be found")
