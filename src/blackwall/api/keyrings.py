#API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

import importlib.util

#Checks if RACFU can be imported
racfu_enabled = importlib.util.find_spec('racfu')

if racfu_enabled:
    from racfu import racfu  # type: ignore
else:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")       

def keyring_exists(keyring: str, owner: str):
    if racfu_enabled:
        result = racfu({"operation": "extract", "admin_type": "keyring", "keyring": keyring.upper(), "owner": owner})
        return result.result["return_codes"]["racf_return_code"] == 0
    else:
        return {}

def get_keyring(keyring: str, owner: str):
    """Extracts information on a keyring"""
    if racfu_enabled:
        result = racfu({"operation": "extract", "admin_type": "keyring", "keyring": keyring.upper(), "owner": owner})
        return result.result
    else:
        return {"": ""}
