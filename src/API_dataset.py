#API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

from dataclasses import dataclass
from API_traits_base import TraitsBase

#Checks if RACFU can be imported
try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")    
    racfu_enabled = False

if racfu_enabled:
    #Dataset functions
    def dataset_profile_exists(dataset: str):
        """Checks if a dataset profile exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "data-set", "profile_name": dataset})
        return result.result["return_codes"]["racf_return_code"] == "0"

    def dataset_profile_get(dataset: str):
        pass

    def dataset_profile_create():
        pass

    def dataset_profile_delete(dataset: str):
        pass

    def dataset_profile_update(dataset: str):
        pass
