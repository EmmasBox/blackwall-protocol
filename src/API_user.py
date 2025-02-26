#User API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

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
class BaseUserTraits(TraitsBase):
    owner: str
    default_group: str
    name: str | None = None

@dataclass
class CICSUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class DCEUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class DFPUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class EIMUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class KerbUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class LanguageUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class LnotesUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class MfaUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class NDSUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class NetviewUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class OMVSUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class OperparmUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class OvmUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class ProxyUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class TSOUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class WorkattrUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None


if racfu_enabled:
    #User functions
    def user_exists(username: str):
        """Checks if a user exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "user", "profile_name": username})
        return result.result["return_codes"]["racf_return_code"] == "0"
        
    def user_get(username: str):
        pass

    def user_create(username: str, base: BaseUserTraits, omvs: OMVSUserTraits | None = None):
        traits = base.to_traits(prefix="base")
        
        if omvs is not None:
            traits.update(omvs.to_traits("omvs"))

        result = racfu(
                {
                    "operation": "add", 
                    "admin_type": "user", 
                    "profile_name": username,
                    "traits":  traits
                }
            )
        pass

    def user_delete(username: str):
        pass

    def user_update(username: str):
        pass