#Permit API module for Blackwall Protocol, this wraps SEAR to increase ease of use and prevent updates from borking everything

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
class BasePermitTraits(TraitsBase):
    access: str | None = field(default=None,metadata={"label": "Data application", "allowed_in": {"alter"}})
    model_profile_class: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    model_profile: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    model_profile_generic: bool | None = field(default=None,metadata={"allowed_in": {"alter"}})
    model_profile_volume: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    reset: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    when_partner_lu_name: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    when_console: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    when_jes: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    when_program: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    when_servauth: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    when_sms: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    when_service: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    when_system: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    when_terminal: str | None = field(default=None,metadata={"allowed_in": {"alter"}})

def update_dataset_permit(dataset: str, racf_id: str, base: BasePermitTraits) -> int:
    """Creates or updates a dataset permit"""
    if sear_enabled:
        traits = base.to_traits(prefix="base")

        result = sear({"operation": "alter", "admin_type": "permission", "data_set": dataset.upper(), "userid": racf_id.upper(), "traits":  traits})
        return result.result["return_codes"]["racf_return_code"]
    else:
        return 8

def delete_dataset_permit(dataset: str, racf_id: str) -> int:
    """Deletes a dataset permit"""
    if sear_enabled:
        result = sear({"operation": "delete", "admin_type": "permission", "data_set": dataset.upper(), "userid": racf_id.upper()})
        return result.result["return_codes"]["racf_return_code"]
    else:
        return 8

def update_resource_permit(profile: str ,class_name: str, racf_id: str, base: BasePermitTraits) -> int:
    """Creates or updates a general resource profile permit"""
    if sear_enabled:
        traits = base.to_traits(prefix="base")

        result = sear({"operation": "alter", "admin_type": "permission", "resource": profile.upper(), "class": class_name.upper(), "userid": racf_id.upper(), "traits":  traits})
        return result.result["return_codes"]["racf_return_code"]
    else:
        return 8

def delete_resource_permit(profile: str, class_name: str, racf_id: str) -> int:
    """Deletes a general resource profile permit"""
    if sear_enabled:
        result = sear({"operation": "delete", "admin_type": "permission", "resource": profile.upper(), "class": class_name.upper(), "userid": racf_id.upper()})
        return result.result["return_codes"]["racf_return_code"]
    else:
        return 8
