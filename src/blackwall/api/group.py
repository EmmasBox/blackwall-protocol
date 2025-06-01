#Group API module for Blackwall Protocol, this wraps SEAR to increase ease of use and prevent updates from borking everything

import importlib.util
from dataclasses import dataclass, field

from .traits_base import TraitsBase

#Checks if SEAR can be imported
sear_enabled = importlib.util.find_spec('sear')

if sear_enabled:
    from sear import sear  # type: ignore
else:
    print("##BLKWL_ERROR_2 Warning: could not find SEAR, entering lockdown mode")       

@dataclass
class BaseGroupTraits(TraitsBase):
    owner: str | None = field(default=None,metadata={"label": "Owner", "allowed_in": {"add","alter","extract"}})
    installation_data: str | None = field(default=None,metadata={"label": "Installation data", "allowed_in": {"add","alter","extract"}})
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
    auto_gid: bool | None = field(default=None,metadata={"label": "Auto GID","allowed_in": {"add","alter"},"invalid_values": {False}})
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
    if sear_enabled:
        result = sear({"operation": "extract", "admin_type": "group", "group": group.upper()})
        return result.result["return_codes"]["racf_return_code"] == 0
    else:
        return False

def get_group(group: str) -> dict:
    """Doesn't handle group profiles that don't exist, recommend using group_exists() first"""
    if sear_enabled:
        result = sear({"operation": "extract", "admin_type": "group", "group": group.upper()})
        return result.result
    else:
        return {}

def get_installation_data(group: str) -> str:
    """Gets the installation data of a group"""
    if sear_enabled:
        result = sear({"operation": "extract", "admin_type": "group", "group": group.upper()})
        if "base:installation_data" in result.result["profile"]["base"]:
            return result.result["profile"]["base"]["base:installation_data"] # type: ignore
        else:
            return ""
    else:
        return ""

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
    if sear_enabled:
        """Creates or updates an existing group"""
        traits = group_object.base_traits.to_traits(prefix="base")

        labels = ["tme","omvs","dfp","ovm"]
        for label in labels:
            trait_object: TraitsBase | None = getattr(group_object,f"{label}_traits")
            if trait_object is not None:
                traits.update(trait_object.to_traits(label))

        operation = "add" if create else "alter"
        
        result = sear(
            {
                "operation": operation, 
                "admin_type": "group", 
                "group": group.upper(),
                "traits":  traits,
            },
        )
        return result.result["return_codes"]["racf_return_code"]

def delete_group(group: str) -> tuple[str, int]:
    if sear_enabled:
        """Deletes a group"""
        result = sear(
            {
                "operation": "delete", 
                "admin_type": "group", 
                "group": group.upper(),
            },
        )
        #TODO add error message
        return "", result.result["return_codes"]["racf_return_code"]
    else:
        return "SEAR can't be found", 8