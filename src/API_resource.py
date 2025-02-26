#General resource API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

from dataclasses import dataclass, fields
from API_traits_base import TraitsBase

#Checks if RACFU can be imported
try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")    
    racfu_enabled = False

if racfu_enabled:
    #General resource profile function
    def resource_profile_exists(resource: str):
        """Checks if a general resource profile exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "resource", "profile_name": resource})
        return result.result["return_codes"]["racf_return_code"] == "0"

    def resource_profile_get(resource: str):
        pass

    def resource_profile_create():
        pass

    def resource_profile_delete(resource: str):
        pass

    def resource_profile_update(resource: str):
        pass