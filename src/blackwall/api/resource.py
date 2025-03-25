#General resource API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

from dataclasses import dataclass, fields
from .traits_base import TraitsBase

#Checks if RACFU can be imported
try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")    
    racfu_enabled = False

if racfu_enabled:
    #General resource profile function
    def resource_profile_exists(resource_class: str,resource: str):
        """Checks if a general resource profile exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "resource", "profile_name": resource})
        return result.result["return_codes"]["racf_return_code"] == "0"

    def resource_profile_get(resource_class: str,resource: str):
        """Doesn't handle general resource profiles that don't exist, recommend using resource_profile_exists() first"""
        #TODO reprogram this bad function
        result = racfu({"operation": "extract", "admin_type": "resource", "profile_name": resource})
        return result.result

    def update_resource_profile(resource_class: str,resource: str):
        pass

    def delete_resource_profile(resource_class: str,resource: str):
        result = racfu(
                {
                    "operation": "delete", 
                    "admin_type": "resource", 
                    "profile_name": resource,
                    "class_name": resource_class
                }
            )
        return result.result["return_codes"]["racf_return_code"] == 0
