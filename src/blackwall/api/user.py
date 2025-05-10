#User API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

import importlib.util
from dataclasses import dataclass, field
from typing import Any

from .traits_base import TraitsBase

#Checks if RACFU can be imported
racfu_enabled = importlib.util.find_spec('racfu')

if racfu_enabled:
    from racfu import racfu  # type: ignore
else:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")       

@dataclass
class BaseUserTraits(TraitsBase):
    #primary
    owner: str | None = field(default=None,metadata={"label": "Owner", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    default_group: str | None = field(default=None,metadata={"label": "Default group", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    name: str | None = field(default=None,metadata={"label": "Name", "input_args": {"max_length": 20,"classes": "field-medium-generic"}})
    installation_data: str | None = field(default=None,metadata={"label": "Installation data", "input_args": {"max_length": 255,"classes": "field-long-generic"}})

    #user attributes
    special: bool | None = field(default=None,metadata={"label": "Special"})
    operations: bool | None = field(default=None,metadata={"label": "Operations"})
    auditor: bool | None = field(default=None,metadata={"label": "Auditor"})
    audit_responsibility: bool | None = field(default=None,metadata={"label": "Read only auditor"})

    password: str | None = field(default=None, metadata={
        "masked": True,
        "maximum": 8,
    })
    
    passphrase: str | None = field(default=None, metadata={
        "masked": True,
        "minimum": 12,
    })
    
    default_group_authority: str | None = field(default=None,metadata={"label": "Default group authority"})
    security_category: str | None = field(default=None,metadata={"label": "Security category"})
    security_level: str | None = field(default=None,metadata={"label": "Security level"})
    security_label: str | None = field(default=None,metadata={"label": "Security label"})
    class_authorization: str | None = field(default=None)
    universal_access: str | None = field(default=None,metadata={"label": "UACC"})

    model_data_set: str | None = field(default=None,metadata={"label": "Model dataset"})
    group_data_set_access: bool | None = field(default=None,metadata={"label": "Group dataset access"})

    create_date: str | None = field(default=None,metadata={"label": "Create date","allowed_in": {"extract"}})
    last_access_date: str | None = field(default=None,metadata={"label": "Last access date","allowed_in": {"extract"}})
    last_access_time: str | None = field(default=None,metadata={"label": "Last access time","allowed_in": {"extract"}})

    audit_logging: bool | None = field(default=None,metadata={"label": "uaudit","allowed_in": {"alter", "extract"}})

@dataclass
class CICSUserTraits(TraitsBase):
    operator_class: str | None = field(default=None, metadata={"label": "operator class", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    operator_id: str | None = field(default=None, metadata={"label": "operator id", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    operator_priority: str | None = field(default=None, metadata={"label": "operator priority", "input_args": {"max_length": 4,"classes": "field-short-generic"}})
    resource_security_level_key: str | None = field(default=None, metadata={"label": "resource security level key", "input_args": {"classes": "field-long-generic"}})
    resource_security_level_keys: str | None = field(default=None, metadata={"label": "resource security level keys", "input_args": {"classes": "field-long-generic"}})
    timeout: str | None = field(default=None, metadata={"label": "timeout", "input_args": {"max_length": 4,"classes": "field-short-generic"}})
    transaction_security_level_key: str | None = field(default=None, metadata={"label": "transaction security level key", "input_args": {"classes": "field-long-generic"}})
    force_signoff_when_xrf_takeover: bool | None = field(default=None, metadata={"label": "Force signoff when xrf takeover", "input_args": {"classes": "field-long-generic"}})

@dataclass
class DCEUserTraits(TraitsBase):
    auto_login: bool | None = field(default=None, metadata={"label": "auto login"})
    name: str | None = None
    home_cell: str | None = None
    home_cell_uuid: str | None = None
    uuid: str | None = None

@dataclass
class DFPUserTraits(TraitsBase):
    data_application: str | None = field(default=None, metadata={"label": "data application", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    data_class: str | None = field(default=None, metadata={"label": "data class", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    management_class: str | None = field(default=None, metadata={"label": "management class", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    storage_class: str | None = field(default=None, metadata={"label": "storage class", "input_args": {"max_length": 8,"classes": "field-short-generic"}})

@dataclass
class EIMUserTraits(TraitsBase):
    ldap_bind_profile: str | None = field(default=None, metadata={"label": "LDAP bind profile", "input_args": {"max_length": 255,"classes": "field-long-generic"}})

@dataclass
class KerbUserTraits(TraitsBase):
    encryption_algorithm: str | None = field(default=None, metadata={"label": "encryption algorithm", "input_args": {"max_length": 255,"classes": "field-long-generic"}})
    name: str | None = field(default=None, metadata={"label": "name", "input_args": {"max_length": 255,"classes": "field-long-generic"}})
    key_from: str | None = field(default=None, metadata={"allowed_in": {"extract"}, "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    key_version: str | None = field(default=None, metadata={"allowed_in": {"extract"}, "input_args": {"max_length": 3,"classes": "field-short-generic"}})
    max_ticket_life: int | None = field(default=None, metadata={"label": "max ticket life", "input_args": {"max_length": 16,"classes": "field-medium-generic"}})

@dataclass
class LanguageUserTraits(TraitsBase):
    primary: str | None = field(default=None, metadata={"label": "primary language", "input_args": {"max_length": 4,"classes": "field-short-generic"}})
    secondary: str | None = field(default=None, metadata={"label": "secondary language", "input_args": {"max_length": 4,"classes": "field-short-generic"}})

@dataclass
class LnotesUserTraits(TraitsBase):
    zos_short_name: str | None = field(default=None, metadata={"label": "Lotus Notes short name", "input_args": {"max_length": 64,"classes": "field-medium-generic"}})

@dataclass
class MfaUserTraits(TraitsBase):
    factor: str | None = field(default=None, metadata={"label": "factor", "allowed_in": {"alter","extract"}})
    active: bool | None = field(default=None, metadata={"label": "mfa active", "allowed_in": {"alter","extract"}})
    tags: str | None = field(default=None, metadata={"label": "tags", "allowed_in": {"alter"}})
    password_fallback: bool | None = field(default=None, metadata={"label": "password fallback", "allowed_in": {"alter","extract"}})
    mfa_policy: str | None = field(default=None, metadata={"label": "MFA policy", "allowed_in": {"alter","extract"}})

@dataclass
class NDSUserTraits(TraitsBase):
    username: str | None = field(default=None, metadata={"label": "username", "input_args": {"max_length": 255,"classes": "field-long-generic"}})

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
    uid: int | None = field(default=None, metadata={"label": "uid", "input_args": {"classes": "field-long-generic"}})
    auto_uid: bool | None = field(default=None, metadata={"label": "auto uid", "invalid_values": {False}})
    shared: bool | None = field(default=None, metadata={"label": "shared", "invalid_values": {False}})
    home_directory: str | None = field(default=None, metadata={"label": "home directory", "input_args": {"classes": "field-long-generic"}})
    default_shell: str | None = field(default=None, metadata={"label": "default shell", "input_args": {"classes": "field-long-generic"}})
    max_address_space_size: int | None = field(default=None, metadata={"label": "max address space size", "input_args": {"classes": "field-long-generic"}})
    max_cpu_time: int | None = field(default=None, metadata={"label": "home directory", "input_args": {"max_length": 10, "classes": "field-medium-generic"}})
    max_files_per_process: int | None = field(default=None, metadata={"label": "max files per process", "input_args": {"classes": "field-long-generic"}})
    max_file_mapping_pages: int | None = field(default=None, metadata={"label": "max file mapping pages", "input_args": {"classes": "field-long-generic"}})
    max_processes: int | None = field(default=None, metadata={"label": "max processes", "input_args": {"classes": "field-long-generic"}})
    max_shared_memory: int | None = field(default=None, metadata={"label": "max shared memory", "input_args": {"max_length": 10, "classes": "field-medium-generic"}})
    max_non_shared_memory: str | None = field(default=None, metadata={"label": "max non shared memory", "input_args": {"max_length": 10, "classes": "field-medium-generic"}})
    max_threads: int | None = field(default=None, metadata={"label": "max threads", "input_args": {"max_length": 10, "classes": "field-medium-generic"}})

@dataclass
class OperparmUserTraits(TraitsBase):
    alternate_console_group: str | None = field(default=None, metadata={"label": "alternate console group", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    receive_automated_messages: str | None = None
    command_target_system: str | None = None
    receive_delete_operator_messages: str | None = field(default=None, metadata={"label": "receive delete operator messages", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    receive_hardcopy_messages: str | None = None
    receive_internal_console_messages: str | None = None
    console_searching_key: str | None = None
    message_level: str | None = None
    log_command_responses: str | None = None
    message_format: str | None = None
    migration_id: str | None = None
    monitor_event: str | None = None
    message_scope: str | None = None
    console_authority: str | None = None
    receive_routing_code: str | None = None
    message_queue_storage: str | None = None
    receive_undelivered_messages: str | None = None
    receive_unknown_console_id_messages: str | None = None

@dataclass
class OvmUserTraits(TraitsBase):
    file_system_root: str | None = field(default=None, metadata={"label": "file system root", "input_args": {"classes": "field-long-generic"}})
    home_directory: str | None = field(default=None, metadata={"label": "home directory", "input_args": {"classes": "field-long-generic"}})
    default_shell: str | None = field(default=None, metadata={"label": "default shell", "input_args": {"classes": "field-long-generic"}})
    uid: str | None = field(default=None, metadata={"label": "uid", "input_args": {"classes": "field-long-generic"}})

@dataclass
class ProxyUserTraits(TraitsBase):
    bind_distinguished_name: str | None = field(default=None, metadata={"label": "bind distinguished name"})
    bind_password: str | None = field(default=None, metadata={"label": "bind password","input_args": {"password": True}})
    ldap_host: str | None = field(default=None, metadata={"label": "LDAP host"})

@dataclass
class TSOUserTraits(TraitsBase):
    account_number: str | None = field(default=None, metadata={"label": "account number", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    logon_command: str | None = field(default=None, metadata={"label": "logon command", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    sysout_destination_id: str | None = field(default=None, metadata={"label": "sysout destination id", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    hold_class: str | None = field(default=None, metadata={"label": "hold class", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    job_class: str | None = field(default=None, metadata={"label": "job class", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    message_class: str | None = field(default=None, metadata={"label": "message class", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    logon_procedure: str | None = field(default=None, metadata={"label": "logon procedure", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    security_label: str | None = field(default=None, metadata={"label": "security label", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    default_region_size: int | None = field(default=None, metadata={"label": "default region size", "input_args": {"classes": "field-medium-generic"}})
    max_region_size: int | None = field(default=None, metadata={"label": "max region size", "input_args": {"classes": "field-medium-generic"}})
    sysout_class: str | None = field(default=None, metadata={"label": "sysout class", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    data_set_allocation_unit: str | None = field(default=None, metadata={"label": "dataset allocation unit", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    user_data: str | None = field(default=None, metadata={"label": "user data", "input_args": {"max_length": 8,"classes": "field-short-generic"}})

@dataclass
class WorkattrUserTraits(TraitsBase):
    account_number: str | None = field(default=None, metadata={"label": "account number", "input_args": {"max_length": 255,"classes": "field-long-generic"}})
    sysout_building: str | None = field(default=None, metadata={"label": "sysout building", "input_args": {"max_length": 60, "classes": "field-medium-generic"}})
    sysout_department: str | None = field(default=None, metadata={"label": "sysout department", "input_args": {"max_length": 60, "classes": "field-medium-generic"}})
    sysout_user: str | None = field(default=None, metadata={"label": "sysout user", "input_args": {"max_length": 8,"classes": "field-short-generic"}})
    sysout_room: str | None = field(default=None, metadata={"label": "sysout room", "input_args": {"max_length": 60, "classes": "field-medium-generic"}})
    sysout_email: str | None = field(default=None, metadata={"label": "email", "input_args": {"max_length": 255,"classes": "field-long-generic"}})


#User functions
def user_exists(username: str) -> bool:
    """Checks if a user exists, returns true or false"""
    if racfu_enabled:
        result = racfu({"operation": "extract", "admin_type": "user", "userid": username.upper()})
        return result.result["return_codes"]["racf_return_code"] == 0
    else:
        return False
    
def get_user(username: str) -> dict[str, Any]:
    """Doesn't handle users that don't exist, recommend using user_exists() first"""
    if racfu_enabled:
        result = racfu({"operation": "extract", "admin_type": "user", "userid": username.upper()})
        return result.result
    else:
        return False

@dataclass
class UserObject:
    base_traits: BaseUserTraits
    tso_traits: TSOUserTraits | None = None
    omvs_traits: OMVSUserTraits | None = None
    cics_traits: CICSUserTraits | None = None
    kerb_traits: KerbUserTraits | None = None
    eim_traits: EIMUserTraits | None = None
    language_traits: LanguageUserTraits | None = None
    dce_traits: DCEUserTraits | None = None
    dfp_traits: DFPUserTraits | None = None
    nds_traits: NDSUserTraits | None = None
    lnotes_traits: LnotesUserTraits | None = None
    mfa_traits: MfaUserTraits | None = None
    ovm_traits: OvmUserTraits | None = None
    proxy_traits: ProxyUserTraits | None = None
    workattr_traits: WorkattrUserTraits | None = None
    netview_traits: NetviewUserTraits | None = None
    operparm_traits: OperparmUserTraits | None = None

def update_user(
        username: str, 
        create: bool,
        user_object: UserObject,
        ):
    """Update or creates a new user, returns true if the user was successfully created and false if an error code was given"""
    traits = user_object.base_traits.to_traits(prefix="base")
    
    labels = ["cics","dce","dfp","eim","language","lnotes","mfa","nds","netview","omvs","operparm","ovm","proxy","tso","workattr"]
    for label in labels:
        trait_object: TraitsBase | None = getattr(user_object,f"{label}_traits")
        if trait_object is not None:
            traits.update(trait_object.to_traits(label))

    operation = "add" if create else "alter"

    result = racfu(
            {
                "operation": operation, 
                "admin_type": "user", 
                "userid": username,
                "traits":  traits,
            },
        )
    return result.result["return_codes"]["racf_return_code"]

def delete_user(username: str) -> tuple[str, int]:
    if racfu_enabled:
        """Deletes a user"""
        result = racfu(
                {
                    "operation": "delete", 
                    "admin_type": "user", 
                    "userid": username.upper(),
                },
            )
        return result.result["commands"][0]["messages"][0], result.result["return_codes"]["racf_return_code"]
    else:
        return "RACFu can't be found", 8
