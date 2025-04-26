from dataclasses import dataclass

from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widgets import Input, Label, Button, Collapsible
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll

from blackwall.api import resource
from blackwall.emoji import get_emoji
from blackwall.notifications import send_notification
from blackwall.panels.panel_mode import PanelMode

from ..traits_ui import generate_trait_section, get_traits_from_input

class PanelResourceNameAndClass(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Profile name:")
        yield Input(max_length=255,id="resource_profile_name",classes="resource-name-field")
        yield Label("Class:")
        yield Input(max_length=8,id="resource_profile_class",classes="class-field")

class PanelResourceInstallationData(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Installation data:")
        yield Input(max_length=255,id="base_installation_data",classes="installation-data",tooltip="Installation data is an optional piece of data you can assign to a dataset profile. You can use installation data to describe whatever you want, such as owning department or what kind of data it protects")

class PanelResourceSegments(VerticalGroup):
    def compose(self) -> ComposeResult:
        with Collapsible(title="Resource profile segments"):
            yield from generate_trait_section(title="Started task data", prefix="stdata", traits_class=resource.STDATAResourceTraits)
            yield from generate_trait_section(title="ICSF", prefix="icsf", traits_class=resource.ICSFResourceTraits)
            yield from generate_trait_section(title="ICTX", prefix="ictx", traits_class=resource.ICTXResourceTraits)
            yield from generate_trait_section(title="JES", prefix="jes", traits_class=resource.JESResourceTraits)
            yield from generate_trait_section(title="Kerberos", prefix="kerb", traits_class=resource.KerbResourceTraits)
            yield from generate_trait_section(title="EIM", prefix="eim", traits_class=resource.EIMResourceTraits)
            yield from generate_trait_section(title="DLF data", prefix="dlfdata", traits_class=resource.DLFDataResourceTraits)
            yield from generate_trait_section(title="IDTPARMS", prefix="idtparms", traits_class=resource.IDTPARMSResourceTraits)
            yield from generate_trait_section(title="Session", prefix="session", traits_class=resource.SessionResourceTraits)
            yield from generate_trait_section(title="SVFMR", prefix="svfmr", traits_class=resource.SVFMRResourceTraits)
            yield from generate_trait_section(title="Proxy", prefix="proxy", traits_class=resource.ProxyResourceTraits)
            yield from generate_trait_section(title="MF policy", prefix="mfpolicy", traits_class=resource.MFPolicyResourceTraits)
            yield from generate_trait_section(title="SIGVER", prefix="sigver", traits_class=resource.SIGVERResourceTraits)
            yield from generate_trait_section(title="tme", prefix="tme", traits_class=resource.TMEResourceTraits)
            yield from generate_trait_section(title="SSIGNON", prefix="ssignon", traits_class=resource.SSIGNONResourceTraits)
            yield from generate_trait_section(title="Cfdef", prefix="Cfdef", traits_class=resource.CfdefResourceTraits)
            yield from generate_trait_section(title="Class Descriptor Table (CDT) info", prefix="cdtinfo", traits_class=resource.CDTINFOResourceTraits)

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
        yield Button(f"{get_emoji("💾")} Save",action="save",classes="action-button")
        yield Button("Delete",action="delete",variant="error",classes="action-button",disabled=self.delete_is_disabled)

    async def action_save(self):
        await self.app.run_action(self.save_action,default_namespace=self.parent)

    async def action_delete(self):
        await self.app.run_action(self.delete_action,default_namespace=self.parent)

@dataclass
class ResourceInfo:
    mode: PanelMode = PanelMode.create

class PanelResource(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield PanelResourceNameAndClass()
        yield PanelResourceInstallationData()
        yield PanelResourceSegments()
        yield PanelResourceActionButtons(save_action="save_resource_profile", delete_action="delete_resource_profile")

    def action_save_resource_profile(self) -> None:
        resource_profile_name = self.get_child_by_type(PanelResourceNameAndClass).get_child_by_id("resource_profile_name",Input).value
        resource_profile_class = self.get_child_by_type(PanelResourceNameAndClass).get_child_by_id("resource_profile_class",Input).value
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
        mfpolicy_segment = get_traits_from_input(operator,self, prefix="mfpolicy", trait_cls=resource.MFPolicyResourceTraits)
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
            mfpolicy=mfpolicy_segment,
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
                send_notification(self,message=f"Unable to create general resource profile, return code: {result}",severity="error")
        else:
            if result == 0:
                self.notify(f"General resource profile {resource_profile_name} updated, return code: {result}",severity="information")
            else:
                send_notification(self,message=f"Unable to update general resource profile, return code: {result}",severity="error")

    def action_delete_resource_profile(self) -> None:
        pass
