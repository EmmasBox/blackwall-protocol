#API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

import importlib.util
from dataclasses import dataclass, field

from .traits_base import TraitsBase

#Checks if RACFU can be imported
racfu_enabled = importlib.util.find_spec('racfu')

if racfu_enabled:
    from racfu import racfu  # type: ignore
else:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")       

@dataclass
class BaseDatasetTraits(TraitsBase):
    #Add and alter fields
    owner: str | None = field(default=None, metadata={"label": "Owner"})
    audit_alter: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_control: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_none: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_read: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_read: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_update: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    security_category: str | None = field(default=None,metadata={"label": "Security category", "allowed_in": {"alter"}})
    installation_data: str | None = field(default=None,metadata={"label": "Installation data", "allowed_in": {"add","alter"}})
    erase_data_sets_on_delete: bool | None = field(default=None,metadata={"label": "Erase datasets on deletion", "allowed_in": {"add","alter"}})
    model_profile_class: str | None = field(default=None,metadata={"label": "Model profile class", "allowed_in": {"add"}})
    model_profile_generic: str | None = field(default=None,metadata={"label": "Model profile generic", "allowed_in": {"add"}})
    tape_data_set_file_sequence_number: int | None = field(default=None,metadata={"allowed_in": {"add"}})
    model_profile: str | None = field(default=None,metadata={"label": "Model profile", "allowed_in": {"add"}})
    model_profile_volume: str | None = field(default=None,metadata={"label": "Model profile volume", "allowed_in": {"add"}})
    global_audit_alter: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_control: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_none: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_read: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_update: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    level: int | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    data_set_model_profile: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    notify_userid: str | None = field(default=None,metadata={"label": "Notify userid", "allowed_in": {"add","alter"}})
    security_label: str | None = field(default=None,metadata={"label": "Security label", "allowed_in": {"add","alter"}})
    security_level: str | None = field(default=None,metadata={"label": "Security level", "allowed_in": {"add","alter"}})
    racf_indicated_dataset: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    create_only_tape_vtoc_entry: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    universal_access: str | None = field(default=None,metadata={"label": "UACC", "allowed_in": {"add","alter"}})
    data_set_allocation_unit: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    volume: str | None = field(default=None,metadata={"label": "Volume", "allowed_in": {"add","alter","extract"}})
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
    create_date: str | None = field(default=None,metadata={"label": "Creation date", "allowed_in": {"extract"}})
    data_set_type: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    high_level_qualifier_is_group: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    creation_group_name: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    last_change_date: str | None = field(default=None,metadata={"label": "Change date","allowed_in": {"extract"}})
    auditing: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    global_auditing: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    use_tape_data_set_profile: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    resident_volume: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    resident_volumes: str | None = field(default=None,metadata={"allowed_in": {"extract"}})

@dataclass
class DFPDatasetTraits(TraitsBase):
    owner: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    ckds_data_key: str | None = field(default=None,metadata={"allowed_in": {"extract"}})

@dataclass
class TMEDatasetTraits(TraitsBase):
    roles: str | None = field(default=None,metadata={"allowed_in": {"extract"}})

#Dataset functions
def dataset_profile_exists(dataset: str) -> bool:
    """Checks if a dataset profile exists, returns true or false"""
    if racfu_enabled:
        result = racfu({"operation": "extract", "admin_type": "data-set", "data_set": dataset.upper()})
        return result.result["return_codes"]["racf_return_code"] == 0
    else:
        return False

def get_dataset_profile(dataset: str) -> dict:
    """Doesn't handle dataset profiles that don't exist, recommend using dataset_profile_exists() first"""
    if racfu_enabled:
        result = racfu({"operation": "extract", "admin_type": "data-set", "data_set": dataset.upper()})
        return result.result
    else:
        return {}

@dataclass
class DatasetObject:
    base_traits: BaseDatasetTraits

def update_dataset_profile(dataset: str, create: bool, dataset_object: DatasetObject):
    """Creates or updates a dataset profile"""
    if racfu_enabled:
        traits = dataset_object.base_traits.to_traits(prefix="base")
        
        operation = "add" if create else "alter"
        
        result = racfu(
            {
                "operation": operation, 
                "admin_type": "data-set", 
                "data_set": dataset.upper(),
                "traits":  traits,
            },
        )
        return result.result["return_codes"]["racf_return_code"]

def delete_dataset_profile(dataset: str) -> tuple[str, int]:
    """Deletes a dataset profile"""
    if racfu_enabled:
        result = racfu(
                {
                    "operation": "delete", 
                    "admin_type": "data-set", 
                    "data_set": dataset.upper(),
                },
            )
        #TODO add error message
        return "", result.result["return_codes"]["racf_return_code"]
    else:
        return "RACFu can't be found", 8
