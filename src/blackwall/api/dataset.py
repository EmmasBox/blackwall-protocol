#API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

from dataclasses import dataclass, field
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
    owner: str | None = field(default=None)
    audit_alter: str | None = field(default=None)
    audit_control: str | None = field(default=None)
    audit_none: str | None = field(default=None)
    audit_read: str | None = field(default=None)
    audit_read: str | None = field(default=None)
    audit_update: str | None = field(default=None)
    security_category: str | None = field(default=None)
    installation_data: str | None = field(default=None)
    data_set_type: str | None = field(default=None)
    erase_data_sets_on_delete: bool | None = field(default=None)
    model_profile_class: str | None = field(default=None)
    model_profile_generic: str | None = field(default=None)
    tape_data_set_file_sequence_number: int | None = field(default=None)
    model_profile: str | None = field(default=None)
    model_profile_volume: str | None = field(default=None)
    global_audit_alter: str | None = field(default=None)
    global_audit_control: str | None = field(default=None)
    global_audit_none: str | None = field(default=None)
    global_audit_read: str | None = field(default=None)
    global_audit_update: str | None = field(default=None)
    level: int | None = field(default=None)
    data_set_model_profile: str | None = field(default=None)
    notify_userid: str | None = field(default=None)
    auditing: str | None = field(default=None)
    security_label: str | None = field(default=None)
    security_level: str | None = field(default=None)
    racf_indicated_dataset: str | None = field(default=None)
    create_only_tape_vtoc_entry: str | None = field(default=None)
    universal_access: str | None = field(default=None)
    data_set_allocation_unit: str | None = field(default=None)
    volume: str | None = field(default=None)
    warn_on_insufficient_access: str | None = field(default=None)

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
        result = racfu({"operation": "extract", "admin_type": "data-set", "profile_name": dataset.upper()})
        return result.result["return_codes"]["racf_return_code"] == 0

    def dataset_profile_get(dataset: str):
        """Doesn't handle dataset profiles that don't exist, recommend using dataset_profile_exists() first"""
        result = racfu({"operation": "extract", "admin_type": "data-set", "profile_name": dataset.upper()})
        return result.result

    def update_dataset_profile(dataset: str, create: bool, base: BaseDatasetTraits):
        traits = base.to_traits(prefix="base")
        
        if create:
            operation = "add"
        else:
            operation = "alter"
        
        result = racfu(
            {
                "operation": operation, 
                "admin_type": "data-set", 
                "profile_name": dataset,
                "traits":  traits
            }
        )
        return result.result["return_codes"]["racf_return_code"]

    def delete_dataset_profile(dataset: str):
        result = racfu(
                {
                    "operation": "delete", 
                    "admin_type": "data-set", 
                    "profile_name": dataset.upper(),
                }
            )
        return result.result["return_codes"]["racf_return_code"] == 0
