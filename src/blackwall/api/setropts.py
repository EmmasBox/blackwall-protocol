
from dataclasses import dataclass, field
from typing import Any
from .traits_base import TraitsBase

#Checks if RACFU can be imported
try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except ImportError:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")    
    racfu_enabled = False

@dataclass
class BaseSetroptsTraits(TraitsBase):

    application_logon_auditing: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    uncataloged_data_set_access: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    log_racf_command_violations: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    enhanced_generic_naming: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    erase_data_sets_on_delete_all: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    erase_data_sets_on_delete_security_level: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    generic_profile_sharing_classes: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    generic_owner: bool | None = field(default=None,metadata={"allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    list_of_groups_access_checking: bool | None = field(default=None,metadata={"allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    password_history: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    revoke_inactive_userids_interval: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    max_password_change_interval: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    jes_network_user: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    jes_undefined_user: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    kerberos_encryption_level: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    audit_log_always_classes: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    audit_log_default_classes: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    audit_log_failure_classes: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    audit_log_never_classes: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    audit_log_success_classes: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    min_password_change_interval: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    multi_level_security_address_space: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    multi_level_security_file_system: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    multi_level_security_interprocess: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    multi_level_security_file_names: bool | None = field(default=None,metadata={"allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    multi_level_security_logon: bool | None = field(default=None,metadata={"allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    multi_level_security_declassification: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    passphrase_change_interval: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    data_set_single_level_name_prefix_protection: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    primary_language: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    protect_all_data_sets: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    password_encryption_algorithm: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    refresh: bool | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    tape_data_set_security_retention_period: int | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    max_incorrect_password_attempts: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    rvary_status_password_format: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    rvary_status_password: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    rvary_status_password_format: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    rvary_status_password: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    #log_commands_issuesd_by_special_users: bool | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    secondary_language: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    max_session_key_interval: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})

    #security_level_auditing: str | None = field(default=None,metadata={"label": "Security level auditing", "allowed_in": {"alter","extract"}})
    
    terminal_universal_access: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    password_expiration_warning: str | None = field(default=None,metadata={"allowed_in": {"alter","extract"}})
    

    #Bools
    add_creator_to_access_list: bool | None = field(default=None,metadata={"label": "Add creator to access list", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    #Note type in documentation wrong
    automatic_data_set_protection: bool | None = field(default=None,metadata={"label": "Automatic dataset protection", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    security_label_compatibility_mode: bool | None = field(default=None,metadata={"allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    program_control: bool | None = field(default=None,metadata={"label": "Program control", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    tape_data_set_protection: bool | None = field(default=None,metadata={"label": "Tape dataset protection","allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    erase_data_sets_on_delete: bool | None = field(default=None,metadata={"label": "Erase datasets on deletion","allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    log_real_data_set_name: bool | None = field(default=None,metadata={"label": "Log real dataset names", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    log_operator_actions: bool | None = field(default=None,metadata={"label": "Log operator actions","allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    security_label_auditing: bool | None = field(default=None,metadata={"label": "Security label auditing", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    security_label_system: bool | None = field(default=None,metadata={"label": "Security label system", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    security_label_control: bool | None = field(default=None,metadata={"label": "Security label control", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    record_user_verification_statistics: bool | None = field(default=None,metadata={"label": "Record user verification statistics", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    password_rules: bool | None = field(default=None,metadata={"label": "Password rules", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    mixed_case_password_support: bool | None = field(default=None,metadata={"label": "Mixed case password support", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    special_character_password_support: bool | None = field(default=None,metadata={"label": "Special character password support", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    multi_level_security_label_alteration: bool | None = field(default=None,metadata={"allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    profile_modelling: bool | None = field(default=None,metadata={"label": "Profile modelling","allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    profile_modelling_generation_data_group: bool | None = field(default=None,metadata={"allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    profile_modelling_group: bool | None = field(default=None,metadata={"allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    profile_modelling_user: bool | None = field(default=None,metadata={"allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    jes_batch: bool | None = field(default=None,metadata={"label": "JES batch", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    jes_early_verification: bool | None = field(default=None,metadata={"label": "JES early verification", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})
    jes_execution_batch_monitoring: bool | None = field(default=None,metadata={"label": "JES execution monitoring", "allowed_in": {"alter","extract"}, "input_args": {"classes": "generic-checkbox-medium"}})

    active_classes: list[str] | None = field(default=None,metadata={"label": "Active classes", "input_args": {"classes": "list-view-generic"}, "allowed_in": {"alter","extract"}})
    statistics_classes: list[str] | None = field(default=None,metadata={"label": "Statistics classes", "allowed_in": {"alter","extract"}})
    generic_command_classes: list[str] | None = field(default=None,metadata={"label": "Generic command classes", "allowed_in": {"alter","extract"}})
    generic_profile_checking_classes: list[str] | None = field(default=None,metadata={"label": "Generic profile checking classes", "allowed_in": {"alter","extract"}})
    raclist: list[str] | None = field(default=None,metadata={"label": "Raclisted classes", "allowed_in": {"alter","extract"}})
    global_access_classes: list[str] | None = field(default=None,metadata={"label": "Global access classes", "allowed_in": {"alter","extract"}})
    audit_classes: list[str] | None = field(default=None,metadata={"label": "Audit classes", "allowed_in": {"alter","extract"}})

def get_racf_options() -> dict[str, Any]:
    if racfu_enabled:
        """Can be used to extract RACF options"""
        result = racfu({"operation": "extract", "admin_type": "racf-options"}) # type: ignore
        return result.result
    else:
        return {}
    
def get_active_classes() -> list[str]:
    if racfu_enabled:
        """Returns a list of active classes on the system"""
        result = racfu({"operation": "extract", "admin_type": "racf-options"}) # type: ignore
        return result.result["profile"]["base"]["base:active_classes"] # type: ignore
    else:
        return []

def refresh_RACF():
    """Refresh RACF"""
    if racfu_enabled:
        result = racfu(
            {
                "operation": "alter", 
                "admin_type": "racf-options", 
                "traits": {
                    "base:refresh": True
                }
            }
        )
        return result.result["return_codes"]["racf_return_code"] # type: ignore

def update_racf_options(base: BaseSetroptsTraits):
    """Modify RACF options"""
    if racfu_enabled:
        traits = base.to_traits(prefix="base")
        
        result = racfu(
            {
                "operation": "alter", 
                "admin_type": "racf-options", 
                "traits":  traits
            }
        )
        return result.result["return_codes"]["racf_return_code"] # type: ignore