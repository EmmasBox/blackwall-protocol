#Permit API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

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
class BasePermitTraits(TraitsBase):
    access: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
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
    if racfu_enabled:
        traits = base.to_traits(prefix="base")

        result = racfu({"operation": "alter", "admin_type": "permission", "data_set": dataset.upper(), "auth_id": racf_id.upper(), "traits":  traits})
        return result.result["return_codes"]["racf_return_code"] == 0
    else:
        return 8

def delete_dataset_permit(dataset: str, racf_id: str) -> int:
    """Deletes a dataset permit"""
    if racfu_enabled:
        result = racfu({"operation": "delete", "admin_type": "permission", "data_set": dataset.upper(), "auth_id": racf_id.upper()})
        return result.result["return_codes"]["racf_return_code"] == 0
    else:
        return 8

def update_resource_permit(profile: str ,class_name: str, racf_id: str, base: BasePermitTraits) -> int:
    """Creates or updates a general resource profile permit"""
    if racfu_enabled:
        traits = base.to_traits(prefix="base")

        result = racfu({"operation": "alter", "admin_type": "permission", "profile_name": profile.upper(), "class_name": class_name.upper(), "auth_id": racf_id.upper(), "traits":  traits})
        return result.result["return_codes"]["racf_return_code"] == 0
    else:
        return 8

def delete_resource_permit(profile: str, class_name: str, racf_id: str) -> int:
    """Deletes a general resource profile permit"""
    if racfu_enabled:
        result = racfu({"operation": "delete", "admin_type": "permission", "profile_name": profile.upper(), "class_name": class_name.upper(), "auth_id": racf_id.upper()})
        return result.result["return_codes"]["racf_return_code"] == 0
    else:
        return 8
