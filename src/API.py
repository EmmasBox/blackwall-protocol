#API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

#Checks if RACFU can be imported
try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, entering lockdown mode")    
    racfu_enabled = False

if racfu_enabled:
    #User functions
    def user_exists(username: str):
        """Checks if a user exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "user", "profile_name": username})
        return result.result["return_codes"]["racf_return_code"] == "0"
        
    def user_get():
        pass

    def user_create():
        pass

    def user_delete():
        pass

    def user_update():
        pass

    #Dataset functions
    def dataset_profile_exists(dataset: str):
        """Checks if a dataset profile exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "data-set", "profile_name": dataset})
        return result.result["return_codes"]["racf_return_code"] == "0"

    def dataset_profile_get():
        pass

    def dataset_profile_create():
        pass

    def dataset_profile_delete():
        pass

    def dataset_profile_update():
        pass

    #General resource profile function
    def resource_profile_exists(resource: str):
        """Checks if a general resource profile exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "resource", "profile_name": resource})
        return result.result["return_codes"]["racf_return_code"] == "0"

    def resource_profile_get():
        pass

    def resource_profile_create():
        pass

    def resource_profile_delete():
        pass

    def resource_profile_update():
        pass

    #Group functions
    def group_profile_exists(group: str):
        """Checks if a group exists, returns true or false"""
        result = racfu({"operation": "extract", "admin_type": "group", "profile_name": group})
        return result.result["return_codes"]["racf_return_code"] == "0"
    
    def group_get():
        pass

    def group_create():
        pass

    def group_delete():
        pass

    def group_update():
        pass