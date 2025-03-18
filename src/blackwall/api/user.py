#User API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

from dataclasses import dataclass, field
from .traits_base import TraitsBase

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
    special: bool | None = None
    operations: bool | None = None
    auditor: bool | None = None

    password: str | None = field(default=None, metadata={
        "masked": True,
        "maximum": 8,
    })
    
    passphrase: str | None = field(default=None, metadata={
        "masked": True,
        "minimum": 12,
    })
    
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
    max_ticket_life: int | None = None

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
    uid: int | None = None
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
    alternate_console_group: str | None = None
    receive_automated_messages: str | None = None
    command_target_system: str | None = None
    receive_delete_operator_messages: str | None = None
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
    account_number: str | None = None
    logon_command: str | None = None
    sysout_destination_id: str | None = None
    hold_class: str | None = None
    job_class: str | None = None
    max_region_size: int | None = None
    message_class: str | None = None
    logon_procedure: str | None = None
    security_label: str | None = None
    default_region_size: int | None = None
    sysout_class: str | None = None
    data_set_allocation_unit: str | None = None
    user_data: str | None = None

@dataclass
class WorkattrUserTraits(TraitsBase):
    account_number: str | None = None
    sysout_building: str | None = None
    sysout_department: str | None = None
    sysout_user: str | None = None
    sysout_room: str | None = None
    sysout_email: str | None = None

if racfu_enabled:
    #User functions
    def user_exists(username: str):
        """Checks if a user exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "user", "profile_name": username})
        return result.result["return_codes"]["racf_return_code"] == 0
        
    def user_get(username: str):
        """Doesn't handle users that don't exist, recommend using user_exists() first"""
        result = racfu({"operation": "extract", "admin_type": "user", "profile_name": username})
        return result.result

    def update_user(
            username: str, 
            create: bool,
            base: BaseUserTraits, 
            cics: CICSUserTraits | None = None, 
            dce: DCEUserTraits | None = None, 
            dfp: DFPUserTraits | None = None, 
            eim: EIMUserTraits | None = None, 
            language: LanguageUserTraits | None = None, 
            lnotes: LnotesUserTraits | None = None, 
            mfa: MfaUserTraits | None = None, 
            nds: NDSUserTraits | None = None, 
            netview: NetviewUserTraits | None = None, 
            omvs: OMVSUserTraits | None = None,
            operparm: OperparmUserTraits | None = None, 
            ovm: OvmUserTraits | None = None, 
            proxy: ProxyUserTraits | None = None, 
            tso: TSOUserTraits | None = None, 
            workattr: WorkattrUserTraits | None = None, 
            ):
        """Update or creates a new user, returns true if the user was successfully created and false if an error code was given"""
        traits = base.to_traits(prefix="base")
        
        if cics is not None:
            traits.update(cics.to_traits("cics"))

        if dce is not None:
            traits.update(dce.to_traits("dce"))

        if dfp is not None:
            traits.update(dfp.to_traits("dfp"))

        if eim is not None:
            traits.update(eim.to_traits("eim"))

        if language is not None:
            traits.update(language.to_traits("language"))

        if lnotes is not None:
            traits.update(lnotes.to_traits("lnotes"))

        if mfa is not None:
            traits.update(mfa.to_traits("mfa"))

        if nds is not None:
            traits.update(nds.to_traits("nds"))

        if netview is not None:
            traits.update(netview.to_traits("netview"))

        if omvs is not None:
            traits.update(omvs.to_traits("omvs"))

        if operparm is not None:
            traits.update(operparm.to_traits("operparm"))

        if ovm is not None:
            traits.update(ovm.to_traits("ovm"))

        if proxy is not None:
            traits.update(proxy.to_traits("proxy"))

        if tso is not None:
            traits.update(tso.to_traits("tso"))
        
        if workattr is not None:
            traits.update(workattr.to_traits("workattr"))

        if create:
            operation = "add"
        else:
            operation = "alter"

        result = racfu(
                {
                    "operation": operation, 
                    "admin_type": "user", 
                    "profile_name": username,
                    "traits":  traits
                }
            )
        return result.result["return_codes"]["racf_return_code"]

    def delete_user(username: str):
        result = racfu(
                {
                    "operation": "delete", 
                    "admin_type": "user", 
                    "profile_name": username,
                }
            )
        return result.result["return_codes"]["racf_return_code"] == 0
