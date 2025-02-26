#Group API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

from dataclasses import dataclass
from API_traits_base import TraitsBase

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
    default_group: str
    name: str | None = None

@dataclass
class DFPGroupTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class OMVSGroupTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class OVMGroupTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class TMEGroupTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None


if racfu_enabled:
    #Group functions
    def group_profile_exists(group: str):
        """Checks if a group exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "group", "profile_name": group})
        return result.result["return_codes"]["racf_return_code"] == "0"
    
    def group_get(group: str):
        pass

    def group_create():
        pass

    def group_delete(group: str):
        pass

    def group_update(group: str):
        pass