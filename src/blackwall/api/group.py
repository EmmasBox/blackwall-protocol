#Group API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

from dataclasses import dataclass, field
from .traits_base import TraitsBase

#Checks if RACFU can be imported
try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except ImportError:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")    
    racfu_enabled = False

@dataclass
class BaseGroupTraits(TraitsBase):
    owner: str
    installation_data: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    data_set_model: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    superior_group: str
    terminal_universal_access: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    universal: str | None = field(default=None,metadata={"allowed_in": {"add","extract"}})

@dataclass
class DFPGroupTraits(TraitsBase):
    data_application: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    data_class: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    management_class: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    storage_class: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class OMVSGroupTraits(TraitsBase):
    auto_gid: str | None = field(default=None,metadata={"allowed_in": {"add","alter"},"invalid_values": {False}})
    gid: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    shared: str | None = field(default=None,metadata={"allowed_in": {"add","alter"},"invalid_values": {False}})

@dataclass
class OVMGroupTraits(TraitsBase):
    gid: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class TMEGroupTraits(TraitsBase):
    roles: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

if racfu_enabled:
    #Group functions
    def group_profile_exists(group: str):
        """Checks if a group exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "group", "profile_name": group})
        return result.result["return_codes"]["racf_return_code"] == 0
    
    def group_get(group: str):
        pass

    def group_get_connections(group: str):
        """Get information on group connections"""
        pass

    def update_group(group: str,create: bool, base: BaseGroupTraits, tme: TMEGroupTraits, omvs: OMVSGroupTraits, dfp: DFPGroupTraits, ovm: OVMGroupTraits):
        traits = base.to_traits(prefix="base")
        
        if tme is not None:
            traits.update(tme.to_traits("tme"))
    
        if dfp is not None:
            traits.update(dfp.to_traits("dfp"))

        if omvs is not None:
            traits.update(omvs.to_traits("omvs"))
    
        if ovm is not None:
            traits.update(ovm.to_traits("ovm"))

        if create:
            operation = "add"
        else:
            operation = "alter"
        
        result = racfu(
            {
                "operation": operation, 
                "admin_type": "group", 
                "profile_name": group,
                "traits":  traits
            }
        )
        return result.result["return_codes"]["racf_return_code"]
    

    def delete_group(group: str):
        result = racfu(
            {
                "operation": "delete", 
                "admin_type": "group", 
                "profile_name": group
            }
        )
        return result.result["return_codes"]["racf_return_code"]