#Group API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

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
class BaseGroupTraits(TraitsBase):
    owner: str | None = field(default=None,metadata={"label": "Owner", "allowed_in": {"add","alter","extract"}})
    installation_data: str | None = field(default=None,metadata={"label": "Intallation data", "allowed_in": {"add","alter","extract"}})
    data_set_model: str | None = field(default=None,metadata={"label": "Dataset model", "allowed_in": {"add","alter","extract"}})
    superior_group: str | None = field(default=None,metadata={"label": "Superior group","allowed_in": {"add","alter","extract"}})
    terminal_universal_access: bool | None = field(default=None,metadata={"label": "Terminal universal access","allowed_in": {"add","alter","extract"}})
    universal: str | None = field(default=None,metadata={"allowed_in": {"add","extract"}})
    subgroups: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    subgroup: str | None = field(default=None,metadata={"label": "Subgroup","allowed_in": {"extract"}})
    connected_users: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    connected_user_authority: str | None = field(default=None,metadata={"label": "Connected user authority","allowed_in": {"extract"}})
    connected_userid: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    create_date: str | None = field(default=None,metadata={"allowed_in": {"extract"}})

@dataclass
class DFPGroupTraits(TraitsBase):
    data_application: str | None = field(default=None,metadata={"label": "Data application", "allowed_in": {"add","alter","extract"}, "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    data_class: str | None = field(default=None,metadata={"label": "Data class", "allowed_in": {"add","alter","extract"}, "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    management_class: str | None = field(default=None,metadata={"label": "Management class", "allowed_in": {"add","alter","extract"}, "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    storage_class: str | None = field(default=None,metadata={"label": "Storage class", "allowed_in": {"add","alter","extract"}, "input_args": {"max_length": 8,"classes": "field-short-generic"}})

@dataclass
class OMVSGroupTraits(TraitsBase):
    auto_gid: str | None = field(default=None,metadata={"allowed_in": {"add","alter"},"invalid_values": {False}})
    gid: int | None = field(default=None,metadata={"label": "GID", "input_args": {"max_length": 10,"classes": "field-medium-generic"}, "allowed_in": {"add","alter","extract"}})
    shared: str | None = field(default=None,metadata={"allowed_in": {"add","alter"},"invalid_values": {False}})

@dataclass
class OVMGroupTraits(TraitsBase):
    gid: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class TMEGroupTraits(TraitsBase):
    roles: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

#Group functions
def group_exists(group: str) -> bool:
    """Checks if a group exists, returns true or false"""
    if racfu_enabled:
        result = racfu({"operation": "extract", "admin_type": "group", "group": group.upper()})
        return result.result["return_codes"]["racf_return_code"] == 0
    else:
        return False

def get_group(group: str) -> dict:
    """Doesn't handle group profiles that don't exist, recommend using group_exists() first"""
    if racfu_enabled:
        result = racfu({"operation": "extract", "admin_type": "group", "group": group.upper()})
        return result.result
    else:
        return {}

def get_group_connections(group: str):
    """Get information on group connections"""
    pass

@dataclass
class GroupObject:
    base_traits: BaseGroupTraits
    tme_traits: TMEGroupTraits | None = None
    omvs_traits: OMVSGroupTraits | None = None
    dfp_traits: DFPGroupTraits | None = None
    ovm_traits: OVMGroupTraits | None = None

def update_group(group: str,create: bool, group_object: GroupObject):
    if racfu_enabled:
        """Creates or updates an existing group"""
        traits = group_object.base_traits.to_traits(prefix="base")

        labels = ["tme","omvs","dfp","ovm"]
        for label in labels:
            trait_object: TraitsBase | None = getattr(group_object,f"{label}_traits")
            if trait_object is not None:
                traits.update(trait_object.to_traits(label))

        operation = "add" if create else "alter"
        
        result = racfu(
            {
                "operation": operation, 
                "admin_type": "group", 
                "group": group.upper(),
                "traits":  traits,
            },
        )
        return result.result["return_codes"]["racf_return_code"]

def delete_group(group: str) -> tuple[str, int]:
    if racfu_enabled:
        """Deletes a group"""
        result = racfu(
            {
                "operation": "delete", 
                "admin_type": "group", 
                "group": group.upper(),
            },
        )
        #TODO add error message
        return "", result.result["return_codes"]["racf_return_code"]
    else:
        return "RACFu can't be found", 8