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
    single_data_set_tape_volume: bool | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    time_zone: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    universal_access: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    warn_on_insufficient_access: bool | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    terminal_access_allowed_day: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    terminal_access_allowed_time: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})

    tape_vtoc: bool | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

    #add fields
    model_profile: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    model_profile_class: str | None = field(default=None,metadata={"allowed_in": {"add"}})
    model_profile_generic: bool | None = field(default=None,metadata={"allowed_in": {"add"}})
    model_profile_volume: str | None = field(default=None,metadata={"allowed_in": {"add"}})

    #alter fields
    global_audit_alter: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_control: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_none: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_read: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    global_audit_update: str | None = field(default=None,metadata={"allowed_in": {"alter"}})
    volume: str | None = field(default=None,metadata={"allowed_in": {"alter"}})

    #extraction fields
    access_list: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    access_count: int | None = field(default=None,metadata={"allowed_in": {"extract"}})
    access_type: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    access_id: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    alter_access_count: int | None = field(default=None,metadata={"allowed_in": {"extract"}})
    control_access_count: int | None = field(default=None,metadata={"allowed_in": {"extract"}})
    read_access_count: int | None = field(default=None,metadata={"allowed_in": {"extract"}})
    update_access_count: int | None = field(default=None,metadata={"allowed_in": {"extract"}})
    security_categories: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    create_date: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    is_generic: bool | None = field(default=None,metadata={"allowed_in": {"extract"}})
    last_change_date: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    last_reference_date: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    member_class_names: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    auditing: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    global_auditing: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    volumes: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    terminal_access_allowed_days: str | None = field(default=None,metadata={"allowed_in": {"extract"}})

@dataclass
class KerbResourceTraits(TraitsBase):
    validate_addresses: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    default_ticket_life: int | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    encryption_algorithm: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    encryption_algorithms: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    realm_name: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    key_version: str | None = field(default=None,metadata={"allowed_in": {"extract"}})
    max_ticket_life: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    min_ticket_life: list[str] | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    password: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})

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
    icsf_key_label: str | None = field(default=None,metadata={"label": "ICSF key label","allowed_in": {"add","alter","extract"}})

@dataclass
class ICSFResourceTraits(TraitsBase):
    certificate_label: str | None = field(default=None,metadata={"label": "Certificate label","allowed_in": {"add","alter","extract"}})
    certificate_labels: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    exportable_public_keys: str | None = field(default=None,metadata={"label": "Exportable public keys","allowed_in": {"add","alter","extract"}})
    symmetric_export_public_key: str | None = field(default=None,metadata={"label": "Symmetric export public key","allowed_in": {"add","alter","extract"}})
    symmetric_export_public_keys: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    symmetric_cpacf_rewrap: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    symmetric_cpacf_rewrap_return: bool | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    asymetric_key_usage: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    key_usage_options: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})

@dataclass
class ICTXResourceTraits(TraitsBase):
    identity_map_timeout: int | None = field(default=None,metadata={"label": "Identity map timeout","allowed_in": {"add","alter","extract"}})
    use_identity_map: bool | None = field(default=None,metadata={"label": "Use identity map","allowed_in": {"add","alter","extract"}})
    require_identity_mapping: bool | None = field(default=None,metadata={"label": "Require identity mapping","allowed_in": {"add","alter","extract"}})
    cache_application_provided_identity_map: bool | None = field(default=None,metadata={"label": "Cache application provided identity map","allowed_in": {"add","alter","extract"}})

@dataclass
class IDTPARMSResourceTraits(TraitsBase):
    signature_algorithm: str | None = field(default=None,metadata={"label": "Signature algorithm", "allowed_in": {"add","alter","extract"}})
    identity_token_timeout: int | None = field(default=None,metadata={"label": "Identity token timeout","allowed_in": {"add","alter","extract"}})
    use_for_any_application: str | None = field(default=None,metadata={"label": "Use for any application","allowed_in": {"add","alter","extract"}})

@dataclass
class SessionResourceTraits(TraitsBase):
    security_checking_level: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    session_key_interval: int | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    locked: bool | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    session_key: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class SVFMRResourceTraits(TraitsBase):
    parameter_list_name: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    script_name: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class STDATAResourceTraits(TraitsBase):
    userid: str | None = field(default=None,metadata={"label": "User ID","allowed_in": {"add","alter","extract"}})
    group: str | None = field(default=None,metadata={"label": "Group","allowed_in": {"add","alter","extract"}})
    privileged: bool | None = field(default=None,metadata={"label": "Privileged","allowed_in": {"add","alter","extract"}})
    trace: bool | None = field(default=None,metadata={"label": "Trace","allowed_in": {"add","alter","extract"}})
    trusted: bool | None = field(default=None,metadata={"label": "Trusted","allowed_in": {"add","alter","extract"}})

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
    reuse_token: bool | None = field(default=None,metadata={"label": "Re-use token","allowed_in": {"add","alter","extract"}})

@dataclass
class SIGVERResourceTraits(TraitsBase):
    fail_program_load_condition: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    log_signature_verification_events: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    signature_required: bool | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

@dataclass
class CDTINFOResourceTraits(TraitsBase):
    case_allowed: str | None = field(default=None,metadata={"label": "Case allowed", "allowed_in": {"add","alter","extract"}})
    default_racroute_return_code: str | None = field(default=None,metadata={"label": "Default racroute return code", "allowed_in": {"add","alter","extract"}})
    valid_first_character: str | None = field(default=None,metadata={"label": "Valid first character","allowed_in": {"add","alter","extract"}})
    valid_first_characters: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    generic_profile_checking: str | None = field(default=None,metadata={"label": "Generic profile checking","allowed_in": {"add","alter","extract"}})
    generic_profile_sharing: str | None = field(default=None,metadata={"label": "Generic profile sharing","allowed_in": {"add","alter","extract"}})
    grouping_class_name: str | None = field(default=None,metadata={"label": "Grouping class name","allowed_in": {"add","alter","extract"}})
    key_qualifiers: str | None = field(default=None,metadata={"label": "Key qualifiers","allowed_in": {"add","alter","extract"}})
    manditory_access_control_processing: str | None = field(default=None,metadata={"label": "Mandatory access control processing","allowed_in": {"add","alter","extract"}})
    max_length: int | None = field(default=None,metadata={"label": "Max length", "allowed_in": {"add","alter","extract"}})
    max_length_entityx: int | None = field(default=None,metadata={"label": "Max length entityx", "allowed_in": {"add","alter","extract"}})
    member_class_name: str | None = field(default=None,metadata={"label": "Member class name","allowed_in": {"add","alter","extract"}})
    operations: str | None = field(default=None,metadata={"label": "Operations","allowed_in": {"add","alter","extract"}})
    valid_other_character: str | None = field(default=None,metadata={"label": "Valid other character","allowed_in": {"add","alter","extract"}})
    valid_other_characters: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    posit_number: int | None = field(default=None,metadata={"label": "Posit number","allowed_in": {"add","alter","extract"}})
    profiles_allowed: str | None = field(default=None,metadata={"label": "Profiles allowed","allowed_in": {"add","alter","extract"}})
    raclist_allowed: str | None = field(default=None,metadata={"label": "Raclist allowed","allowed_in": {"add","alter","extract"}})
    send_enf_signal_on_profile_creation: str | None = field(default=None,metadata={"label": "Send enf signal on profile creation", "allowed_in": {"add","alter","extract"}})
    security_label_required: str | None = field(default=None,metadata={"label": "Security label required","allowed_in": {"add","alter","extract"}})
    default_universal_access: str | None = field(default=None,metadata={"label": "Default universal access","allowed_in": {"add","alter","extract"}})

@dataclass
class TMEResourceTraits(TraitsBase):
    child: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    group: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    parent: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    resource: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    role: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

    children: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    groups: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    resources: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})
    roles: list[str] | None = field(default=None,metadata={"allowed_in": {"extract"}})

@dataclass
class SSIGNONResourceTraits(TraitsBase):
    enhanced_pass_ticket_label: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    enhanced_pass_ticket_type: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    enhanced_pass_ticket_timeout: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    enhanced_pass_ticket_replay: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    legacy_pass_ticket_label: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

    mask_legacy_pass_ticket_key: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})
    encrypt_legacy_pass_ticket_key: str | None = field(default=None,metadata={"allowed_in": {"add","alter"}})

@dataclass
class CfdefResourceTraits(TraitsBase):
    custom_field_data_type: str | None = field(default=None,metadata={"allowed_in": {"add","extract"}})
    valid_first_characters: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    help_text: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    list_heading_text: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    mixed_case_allowed: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    min_numeric_value: int | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    max_field_length: int | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    max_numeric_value: int | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    valid_other_characters: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})
    validation_rexx_exec: str | None = field(default=None,metadata={"allowed_in": {"add","alter","extract"}})

#Checks if RACFU can be imported
try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except ImportError:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")    
    racfu_enabled = False


#General resource profile function
def resource_profile_exists(resource_class: str,resource: str) -> bool:
    if racfu_enabled:
        """Checks if a general resource profile exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "resource", "profile_name": resource}) # type: ignore
        return result.result["return_codes"]["racf_return_code"] == 0
    else:
        return False

def get_resource_profile(resource_class: str,resource: str):
    if racfu_enabled:
        """Doesn't handle general resource profiles that don't exist, recommend using resource_profile_exists() first"""
        result = racfu({"operation": "extract", "admin_type": "resource", "profile_name": resource}) # type: ignore
        return result.result

def update_resource_profile(
        resource_class: str,
        resource: str, 
        create: bool, 
        base: BaseResourceTraits,
        stdata: STDATAResourceTraits | None = None,
        cdtinfo: CDTINFOResourceTraits | None = None,
        kerb: KerbResourceTraits | None = None,
        tme: TMEResourceTraits | None = None,
        ssignon: SSIGNONResourceTraits | None = None,
        proxy: ProxyResourceTraits | None = None,
        icsf: ICSFResourceTraits | None = None,
        ictx: ICTXResourceTraits | None = None,
        svfmr: SVFMRResourceTraits | None = None,
        sigver: SIGVERResourceTraits | None = None,
        mfapolicy: MFAPolicyResourceTraits | None = None,
        session: SessionResourceTraits | None = None,
        idtparms: IDTPARMSResourceTraits | None = None,
        jes: JESResourceTraits | None = None,
        dlfdata: DLFDataResourceTraits | None = None,
        cfdef: CfdefResourceTraits | None = None,
        eim: EIMResourceTraits | None = None,
        ):
    traits = base.to_traits(prefix="base")

    if stdata is not None:
        traits.update(stdata.to_traits("stdata"))

    if cdtinfo is not None:
        traits.update(cdtinfo.to_traits("cdtinfo"))

    if ssignon is not None:
        traits.update(ssignon.to_traits("ssignon"))

    if sigver is not None:
        traits.update(sigver.to_traits("sigver"))

    if svfmr is not None:
        traits.update(svfmr.to_traits("svfmr"))

    if tme is not None:
        traits.update(tme.to_traits("tme"))

    if kerb is not None:
        traits.update(kerb.to_traits("kerb"))

    if proxy is not None:
        traits.update(proxy.to_traits("proxy"))

    if icsf is not None:
        traits.update(icsf.to_traits("icsf"))

    if ictx is not None:
        traits.update(ictx.to_traits("ictx"))

    if mfapolicy is not None:
        traits.update(mfapolicy.to_traits("mfapolicy"))

    if session is not None:
        traits.update(session.to_traits("session"))

    if idtparms is not None:
        traits.update(idtparms.to_traits("idtparms"))

    if jes is not None:
        traits.update(jes.to_traits("jes"))

    if dlfdata is not None:
        traits.update(dlfdata.to_traits("dlfdata"))

    if cfdef is not None:
        traits.update(cfdef.to_traits("cfdef"))

    if eim is not None:
        traits.update(eim.to_traits("eim"))

    if create:
        operation = "add"
    else:
        operation = "alter"
    
    result = racfu( # type: ignore
        {
            "operation": operation, 
            "admin_type": "resource", 
            "profile_name": resource,
            "class_name": resource_class,
            "traits":  traits
        }
    )
    return result.result["return_codes"]["racf_return_code"]

def delete_resource_profile(resource_class: str,resource: str) -> int:
    if racfu_enabled:
        result = racfu( # type: ignore
                {
                    "operation": "delete", 
                    "admin_type": "resource", 
                    "profile_name": resource,
                    "class_name": resource_class
                }
            )
        return result.result["return_codes"]["racf_return_code"] == 0
    else:
        return 8
