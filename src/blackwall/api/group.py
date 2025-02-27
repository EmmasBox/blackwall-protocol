#Group API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

from dataclasses import dataclass
from .traits_base import TraitsBase

#Checks if RACFU can be imported
try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")    
    racfu_enabled = False

@dataclass
class BaseGroupTraits(TraitsBase):
    owner: str
    installation_data: str | None = None
    superior_group: str
    terminal_universal_access: str | None = None
    universal: str | None = None

@dataclass
class DFPGroupTraits(TraitsBase):
    data_application: str | None = None
    data_class: str | None = None
    management_class: str | None = None
    storage_class: str | None = None

@dataclass
class OMVSGroupTraits(TraitsBase):
    auto_gid: str | None = None
    gid: str | None = None
    shared: str | None = None

@dataclass
class OVMGroupTraits(TraitsBase):
    gid: str | None = None
    home_directory: str | None = None

@dataclass
class TMEGroupTraits(TraitsBase):
    roles: str | None = None

if racfu_enabled:
    #Group functions
    def group_profile_exists(group: str):
        """Checks if a group exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "group", "profile_name": group})
        return result.result["return_codes"]["racf_return_code"] == "0"
    
    def group_get(group: str):
        pass

    def group_get_connections(group: str):
        """Get information on group connections"""
        pass

    def group_create():
        pass

    def group_delete(group: str):
        pass

    def group_update(group: str):
        pass