#User API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

from dataclasses import dataclass
from API_traits_base import TraitsBase

#Checks if RACFU can be imported
try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")    
    racfu_enabled = False

@dataclass
class BaseUserTraits(TraitsBase):
    #primary
    owner: str
    default_group: str
    name: str | None = None
    installation_data: str | None = None

    #user attributes
    special: str | None = None 
    operations: str | None = None 
    auditor: str | None = None
    
    default_group_authority: str | None = None
    security_category: str | None = None
    security_categories: str | None = None
    class_authorization: str | None = None

@dataclass
class CICSUserTraits(TraitsBase):
    operator_class: str | None = None
    operator_id: str | None = None
    operator_priority: str | None = None
    resource_security_level_key: str | None = None
    resource_security_level_keys: str | None = None
    timeout: str | None = None
    transaction_security_level_key: str | None = None
    force_signoff_when_xrf_takeover: bool | None = None

@dataclass
class DCEUserTraits(TraitsBase):
    auto_login: bool | None = None
    name: str | None = None
    home_cell: str | None = None
    home_cell_uuid: str | None = None
    uuid: str | None = None

@dataclass
class DFPUserTraits(TraitsBase):
    data_application: str | None = None
    data_class: str | None = None
    management_class: str | None = None
    storage_class: str | None = None

@dataclass
class EIMUserTraits(TraitsBase):
    ldap_bind_profile: str | None = None

@dataclass
class KerbUserTraits(TraitsBase):
    encryption_algorithm: str | None = None
    name: str | None = None
    key_from: str | None = None
    key_version: str | None = None
    max_ticket_life: str | None = None

@dataclass
class LanguageUserTraits(TraitsBase):
    primary: str | None = None
    secondary: str | None = None

@dataclass
class LnotesUserTraits(TraitsBase):
    zos_short_name: str | None = None

@dataclass
class MfaUserTraits(TraitsBase):
    factor: str | None = None
    active: bool | None = None
    tags: str | None = None
    password_fallback: bool | None = None
    mfa_policy: str | None = None

@dataclass
class NDSUserTraits(TraitsBase):
    username: str | None = None

@dataclass
class NetviewUserTraits(TraitsBase):
    default_mcs_console_name: str | None = None
    security_control_check: str | None = None
    domain: str | None = None
    logon_commands: str | None = None
    receive_unsolicited_messages: str | None = None
    operator_graphic_monitor_facility_administration_allowed: str | None = None
    operator_graphic_monitor_facility_display_authority: str | None = None
    operator_scope_classes: str | None = None

@dataclass
class OMVSUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None
    auto_uid: bool | None = None
    max_address_space_size: int | None = None
    max_cpu_time: int | None = None
    max_files_per_process: int | None = None
    home_directory: str | None = None
    max_non_shared_memory: str | None = None
    max_file_mapping_pages: int | None = None
    max_processes: int | None = None
    default_shell: str | None = None
    shared: bool | None = None
    max_shared_memory: int | None = None
    max_threads: int | None = None

@dataclass
class OperparmUserTraits(TraitsBase):
    pass

@dataclass
class OvmUserTraits(TraitsBase):
    file_system_root: str | None = None
    home_directory: str | None = None
    default_shell: str | None = None
    uid: str | None = None

@dataclass
class ProxyUserTraits(TraitsBase):
    bind_distinguished_name: str | None = None
    bind_password: str | None = None
    ldap_host: str | None = None

@dataclass
class TSOUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None

@dataclass
class WorkattrUserTraits(TraitsBase):
    uid: str | None = None
    home_directory: str | None = None


if racfu_enabled:
    #User functions
    def user_exists(username: str):
        """Checks if a user exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "user", "profile_name": username})
        return result.result["return_codes"]["racf_return_code"] == "0"
        
    def user_get(username: str):
        pass

    def user_create(username: str, base: BaseUserTraits, omvs: OMVSUserTraits | None = None):
        traits = base.to_traits(prefix="base")
        
        if omvs is not None:
            traits.update(omvs.to_traits("omvs"))

        result = racfu(
                {
                    "operation": "add", 
                    "admin_type": "user", 
                    "profile_name": username,
                    "traits":  traits
                }
            )
        pass

    def user_delete(username: str):
        pass

    def user_update(username: str):
        pass