#API module for Blackwall Protocol, this wraps SEAR to increase ease of use and prevent updates from borking everything

import importlib.util
from dataclasses import dataclass, field
from typing import Any

from .traits_base import TraitsBase

#Checks if SEAR can be imported
sear_enabled = importlib.util.find_spec('sear')

if sear_enabled:
    from sear import sear  # type: ignore
else:
    print("##BLKWL_ERROR_2 Warning: could not find SEAR, entering lockdown mode")       

@dataclass
class BaseRRSFTraits(TraitsBase):
    #Add and alter fields
    subsystem_name: str | None = field(default=None,metadata={"label": "Sub-system name","allowed_in": {"extract"}})
    subsystem_userid: str | None = field(default=None,metadata={"label": "Sub-system userid","allowed_in": {"extract"}})
    subsystem_operator_prefix: str | None = field(default=None,metadata={"label": "Sub-system operator prefix","allowed_in": {"extract"}})
    number_of_defined_nodes: int | None = field(default=None,metadata={"label": "RRSF nodes defined","allowed_in": {"extract"}})
    nodes: list[Any] | None = field(default=None,metadata={"allowed_in": {"extract"}})

def get_rrsf_options() -> dict[str, Any]:
    """Returns a dict with all of the RRSF options"""
    if sear_enabled:
        """Can be used to extract RRSF options"""
        result = sear({"operation": "extract", "admin_type": "racf-rrsf"}) # type: ignore
        return result.result
    else:
        return {}