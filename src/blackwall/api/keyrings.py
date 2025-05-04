#API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

import importlib.util
from dataclasses import dataclass, field
from typing import Any

from blackwall.api.traits_base import TraitsBase

#Checks if RACFU can be imported
racfu_enabled = importlib.util.find_spec('racfu')

if racfu_enabled:
    from racfu import racfu  # type: ignore
else:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")       

@dataclass
class CertificateTraits:
    DN: str | None = field(default=None,metadata={"label": "DN", "allowed_in": {"extract"}})
    default: str | None = field(default=None,metadata={"label": "Default", "allowed_in": {"extract"}})
    extensions: list[str] | None = field(default=None,metadata={"label": "Extensions", "allowed_in": {"extract"}})
    issuer: str | None = field(default=None,metadata={"label": "Issuer", "allowed_in": {"extract"}})
    keySize: int | None = field(default=None,metadata={"label": "Key size", "allowed_in": {"extract"}})  # noqa: N815
    label: str | None = field(default=None,metadata={"label": "Label", "allowed_in": {"extract"}})
    notAfter: str | None = field(default=None,metadata={"label": "Not after", "allowed_in": {"extract"}})  # noqa: N815
    notBefore: str | None = field(default=None,metadata={"label": "Not before", "allowed_in": {"extract"}})  # noqa: N815
    owner: str | None = field(default=None,metadata={"label": "Owner", "allowed_in": {"extract"}})
    privateKey: str | None = field(default=None,metadata={"label": "Private key", "allowed_in": {"extract"}})  # noqa: N815
    serialNumber: str | None = field(default=None,metadata={"label": "Serial number", "allowed_in": {"extract"}})  # noqa: N815
    version: int | None = field(default=None,metadata={"label": "Version", "allowed_in": {"extract"}})
    usage: str | None = field(default=None,metadata={"label": "Usage", "allowed_in": {"extract"}})
    status: str | None = field(default=None,metadata={"label": "Status", "allowed_in": {"extract"}})
    signature: dict[str, str] | None = field(default=None,metadata={"label": "Signature", "allowed_in": {"extract"}})

@dataclass
class KeyringTraits(TraitsBase):
    ring_name: str | None = field(default=None,metadata={"label": "Ring name", "allowed_in": {"extract"}})
    ring_owner: str | None = field(default=None,metadata={"label": "Ring owner", "allowed_in": {"extract"}})
    certificates: list[CertificateTraits] | None = field(default=None,metadata={"label": "Certificates", "allowed_in": {"extract"}})

@dataclass
class KeyringObject:
    keyring_traits: KeyringTraits
    certificate_traits: CertificateTraits

def keyring_exists(keyring: str, owner: str):
    if racfu_enabled:
        result = racfu({"operation": "extract", "admin_type": "keyring", "keyring": keyring, "owner": owner.upper()})
        return result.result["return_codes"]["racf_return_code"] == 0
    else:
        return {}

def get_keyring(keyring: str, owner: str) -> dict[str, Any]:
    """Extracts information on a keyring"""
    if racfu_enabled:
        result = racfu({"operation": "extract", "admin_type": "keyring", "keyring": keyring, "owner": owner.upper()})
        if result.result is not None:
            return result.result["keyrings"][0]
    return {"": ""}
