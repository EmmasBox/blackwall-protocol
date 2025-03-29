#General resource API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

from dataclasses import dataclass, field
from .traits_base import TraitsBase

@dataclass
class BaseResourceTraits(TraitsBase):
    #add+alter fields
    owner: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_alter: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_control: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_none: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_read: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_read: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    audit_update: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    security_category: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    installation_data: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    level: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    member_class_name: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    notify_userid: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    security_label: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    security_level: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    single_data_set_tape_volume: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    time_zone: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    universal_access: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    warn_on_insufficient_access: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    terminal_access_allowed_day: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    terminal_access_allowed_time: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})

    #add fields
    model_profile: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    model_profile_class: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    model_profile_generic: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    model_profile_volume: str | None = field(default=None,metadata={"allowed_in": {"add"}})

    #alter fields
    global_audit_alter: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_control: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_none: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_read: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_update: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    volume: str | None = field(default=None,metadata={"allowed_in": {"alter"}})

    #extraction fields
    access_list: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    access_count: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    access_type: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    access_id: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    alter_access_count: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    control_access_count: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    read_access_count: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    update_access_count: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    security_categories: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    create_date: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    is_generic: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    last_change_date: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    last_reference_date: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    member_class_names: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    auditing: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    global_auditing: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    volumes: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    terminal_access_allowed_days: str | None = field(default=None,metadata={"allowed_in": {"extract"}})

@dataclass
class DLFDataResourceTraits(TraitsBase):
    job_name: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    job_names: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    retain_object_after_use: bool | None = field(default=None,metadata={"allowed_in": {"add","alter"}})

@dataclass
class EIMResourceTraits(TraitsBase):
    domain_distinguished_name: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    kerberos_registry: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    local_registry: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    options: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class JESResourceTraits(TraitsBase):
    icsf_key_label: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class SVFMRResourceTraits(TraitsBase):
    parameter_list_name: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    script_name: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class STDATAResourceTraits(TraitsBase):
    group: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    privileged: bool | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    trace: bool | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    trusted: bool | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    userid: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class ProxyResourceTraits(TraitsBase):
    bind_distinguished_name: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    bind_password: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    ldap_host: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class MFAPolicyResourceTraits(TraitsBase):
    factor: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    factors: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    token_timeout: int | None = field(default=None,metadata={"allowed_in": {"extract"}})
    reuse_token: bool | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class SIGVERResourceTraits(TraitsBase):
    fail_program_load_condition: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    log_signature_verification_events: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    signature_required: bool | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class CDTINFOResourceTraits(TraitsBase):
    case_allowed: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    default_racroute_return_code: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    valid_first_character: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    valid_first_characters: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    generic_profile_checking: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    generic_profile_sharing: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    grouping_class_name: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    key_qualifiers: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    manditory_access_control_processing: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    max_length: int | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    max_length_entityx: int | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    member_class_name: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    operations: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    valid_other_character: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    valid_other_characters: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    posit_number: int | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    profiles_allowed: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    raclist_allowed: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    send_enf_signal_on_profile_creation: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    security_label_required: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    default_universal_access: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

#Checks if RACFU can be imported
try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")    
    racfu_enabled = False

if racfu_enabled:
    #General resource profile function
    def resource_profile_exists(resource_class: str,resource: str):
        """Checks if a general resource profile exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "resource", "profile_name": resource})
        return result.result["return_codes"]["racf_return_code"] == 0

    def resource_profile_get(resource_class: str,resource: str):
        """Doesn't handle general resource profiles that don't exist, recommend using resource_profile_exists() first"""
        #TODO reprogram this bad function
        result = racfu({"operation": "extract", "admin_type": "resource", "profile_name": resource})
        return result.result

    def update_resource_profile(resource_class: str,resource: str):
        pass

    def delete_resource_profile(resource_class: str,resource: str):
        result = racfu(
                {
                    "operation": "delete", 
                    "admin_type": "resource", 
                    "profile_name": resource,
                    "class_name": resource_class
                }
            )
        return result.result["return_codes"]["racf_return_code"] == 0
