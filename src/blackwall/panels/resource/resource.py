from dataclasses import dataclass

from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.lazy import Lazy

from blackwall.api import resource
from blackwall.panels.panel_mode import PanelMode

from ..traits_ui import generate_trait_section, get_traits_from_input

class PanelResourceClassName(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Profile name:")
        yield Input(max_length=255,id="resource_profile_name",classes="resource-name-field")
        yield Label("Class:")
        yield Input(max_length=8,id="resource_profile_class",classes="class-field")

class PanelResourceInstallationData(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Installation data:")
        yield Input(max_length=255,id="installation_data",classes="installation-data",tooltip="Installation data is an optional piece of data you can assign to a dataset profile. You can use installation data to describe whatever you want, such as owning department or what kind of data it protects")

class PanelResourceSegments(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Lazy(widget=Collapsible(title="Resource profile segments")):
            yield from generate_trait_section(title="stdata", prefix="stdata", traits_class=resource.STDATAResourceTraits)
            yield from generate_trait_section(title="CDT info", prefix="cdtinfo", traits_class=resource.CDTINFOResourceTraits)

class PanelResourceActionButtons(HorizontalGroup):
    edit_mode: reactive[PanelMode] = reactive(PanelMode.create,recompose=True)

    if edit_mode is True:
        delete_is_disabled = False
    else:
        delete_is_disabled = True

    def __init__(self, save_action: str, delete_action: str):
        super().__init__()
        self.save_action = save_action
        self.delete_action = delete_action
    
    def compose(self) -> ComposeResult:
        yield Button("Save",action="save",classes="action-button")
        yield Button("Delete",action="delete",classes="action-button",disabled=self.delete_is_disabled)

    async def action_save(self):
        await self.app.run_action(self.save_action,default_namespace=self.parent)

    async def action_delete(self):
        await self.app.run_action(self.delete_action,default_namespace=self.parent)

@dataclass
class ResourceInfo:
    mode: PanelMode = PanelMode.create

class PanelResource(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelResourceClassName()
        yield PanelResourceInstallationData()
        yield PanelResourceSegments()
        yield PanelResourceActionButtons(save_action="save_resource_profile", delete_action="delete_resource_profile")

    def action_save_resource_profile(self) -> None:
        resource_profile_name = self.query_exactly_one(selector="#resource_profile_name").value
        resource_profile_class = self.query_exactly_one(selector="#resource_profile_class").value
        resource_profile_exists = resource.resource_profile_exists(resource=resource_profile_name,resource_class=resource_profile_class)

        if resource_profile_exists:
            operator = "alter"
        else:
            operator = "add"

        base_segment = get_traits_from_input(operator,self, prefix="base", trait_cls=resource.BaseResourceTraits)
        kerb_segment = get_traits_from_input(operator,self, prefix="kerb", trait_cls=resource.KerbResourceTraits)
        dlfdata_segment = get_traits_from_input(operator,self, prefix="dlfdata", trait_cls=resource.DLFDataResourceTraits)
        eim_segment = get_traits_from_input(operator,self, prefix="eim", trait_cls=resource.EIMResourceTraits)
        jes_segment = get_traits_from_input(operator,self, prefix="jes", trait_cls=resource.JESResourceTraits)
        icsf_segment = get_traits_from_input(operator,self, prefix="icsf", trait_cls=resource.ICSFResourceTraits)
        ictx_segment = get_traits_from_input(operator,self, prefix="ictx", trait_cls=resource.ICTXResourceTraits)
        idtparms_segment = get_traits_from_input(operator,self, prefix="idtparms", trait_cls=resource.IDTPARMSResourceTraits)
        session_segment = get_traits_from_input(operator,self, prefix="session", trait_cls=resource.SessionResourceTraits)
        svfmr_segment = get_traits_from_input(operator,self, prefix="svfmr", trait_cls=resource.SVFMRResourceTraits)
        stdata_segment = get_traits_from_input(operator,self, prefix="stdata", trait_cls=resource.STDATAResourceTraits)
        proxy_segment = get_traits_from_input(operator,self, prefix="proxy", trait_cls=resource.ProxyResourceTraits)
        mfapolicy_segment = get_traits_from_input(operator,self, prefix="mfapolicy", trait_cls=resource.MFAPolicyResourceTraits)
        sigver_segment = get_traits_from_input(operator,self, prefix="sigver", trait_cls=resource.SIGVERResourceTraits)
        tme_segment = get_traits_from_input(operator,self, prefix="tme", trait_cls=resource.TMEResourceTraits)
        cdtinfo_segment = get_traits_from_input(operator,self, prefix="cdtinfo", trait_cls=resource.CDTINFOResourceTraits)
        ssignon_segment = get_traits_from_input(operator,self, prefix="ssignon", trait_cls=resource.SSIGNONResourceTraits)
        cfdef_segment = get_traits_from_input(operator,self, prefix="cfdef", trait_cls=resource.CfdefResourceTraits)

        result = resource.update_resource_profile(
            resource=resource_profile_name,
            resource_class=resource_profile_class,
            create=not resource_profile_exists,
            base=base_segment,
            kerb=kerb_segment,
            cdtinfo=cdtinfo_segment,
            dlfdata=dlfdata_segment,
            eim=eim_segment,
            jes=jes_segment,
            icsf=icsf_segment,
            ictx=ictx_segment,
            idtparms=idtparms_segment,
            session=session_segment,
            svfmr=svfmr_segment,
            stdata=stdata_segment,
            proxy=proxy_segment,
            mfapolicy=mfapolicy_segment,
            sigver=sigver_segment,
            tme=tme_segment,
            ssignon=ssignon_segment,
            cfdef=cfdef_segment
            )
        
        if not resource_profile_exists:
            if (result == 0 or result == 4):
                self.notify(f"General resource profile {resource_profile_name} created, return code: {result}",severity="information")
                #self.set_edit_mode()
            else:
                self.notify(f"Unable to create general resource profile, return code: {result}",severity="error")
        else:
            if (result == 0 or result == 4):
                self.notify(f"General resource profile {resource_profile_name} updated, return code: {result}",severity="information")
            else:
                self.notify(f"Unable to update general resource profile, return code: {result}",severity="error")

    def action_delete_resource_profile(self) -> None:
        pass
