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
    #Add and alter fields
    owner: str | None = field(default=None)
    audit_alter: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_control: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_none: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_read: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_read: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_update: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    security_category: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    installation_data: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    erase_data_sets_on_delete: bool | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    model_profile_class: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    model_profile_generic: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    tape_data_set_file_sequence_number: int | None = field(default=None,metadata={"allowed_in": {"add"}})
    model_profile: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    model_profile_volume: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    global_audit_alter: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_control: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_none: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_read: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_update: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    level: int | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    data_set_model_profile: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    notify_userid: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    security_label: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    security_level: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    racf_indicated_dataset: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    create_only_tape_vtoc_entry: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    universal_access: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    data_set_allocation_unit: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    volume: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    warn_on_insufficient_access: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})

    #Extraction fields
    access_list: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    access_count: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    access_type: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    access_id: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    alter_access_count: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    control_access_count: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    read_access_count: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    update_access_count: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    alter_volume: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    security_categories: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    create_date: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    data_set_type: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    high_level_qualifier_is_group: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    creation_group_name: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    last_change_date: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    auditing: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    global_auditing: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    use_tape_data_set_profile: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    resident_volume: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    resident_volumes: str | None = field(default=None,metadata={"allowed_in": {"extract"}})

#Checks if RACFU can be imported
try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")    
    racfu_enabled = False


#Dataset functions
def dataset_profile_exists(dataset: str):
    """Checks if a dataset profile exists, returns true or false"""
    if racfu_enabled:
        result = racfu({"operation": "extract", "admin_type": "data-set", "profile_name": dataset.upper()})
        return result.result["return_codes"]["racf_return_code"] == 0

def dataset_profile_get(dataset: str):
    #TODO reprogram this bad function
    """Doesn't handle dataset profiles that don't exist, recommend using dataset_profile_exists() first"""
    if racfu_enabled:
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
