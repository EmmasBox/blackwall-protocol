#API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

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
class BaseDatasetTraits(TraitsBase):
    owner: str
    audit_alter: str | None = None
    audit_control: str | None = None
    audit_none: str | None = None
    audit_read: str | None = None
    audit_read: str | None = None
    audit_update: str | None = None
    security_category: str | None = None
    installation_data: str | None = None
    data_set_type: str | None = None
    erase_data_sets_on_delete: bool | None = None
    model_profile_class: str | None = None
    model_profile_generic: str | None = None
    tape_data_set_file_sequence_number: int | None = None
    model_profile: str | None = None
    model_profile_volume: str | None = None
    global_audit_alter: str | None = None
    global_audit_control: str | None = None
    global_audit_none: str | None = None
    global_audit_read: str | None = None
    global_audit_update: str | None = None
    level: int | None = None
    data_set_model_profile: str | None = None
    notify_userid: str | None = None
    auditing: str | None = None
    security_label: str | None = None
    security_level: str | None = None
    racf_indicated_dataset: str | None = None
    create_only_tape_vtoc_entry: str | None = None
    universal_access: str | None = None
    data_set_allocation_unit: str | None = None
    volume: str | None = None
    warn_on_insufficient_access: str | None = None

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
        """Doesn't handle dataset profiles that don't exist, recommend using dataset_profile_exists() first"""
        result = racfu({"operation": "extract", "admin_type": "data-set", "profile_name": dataset})
        return result.result

    def update_dataset_profile():
        pass

    def delete_dataset_profile(dataset: str):
        result = racfu(
                {
                    "operation": "delete", 
                    "admin_type": "data-set", 
                    "profile_name": dataset,
                }
            )
        return result.result["return_codes"]["racf_return_code"] == 0
