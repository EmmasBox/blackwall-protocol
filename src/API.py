#API module for Blackwall Protocol, this wraps RACFU to increase ease of use and prevent updates from borking everything

#Checks if RACFU can be imported
try:
    from racfu import racfu # type: ignore
    racfu_enabled = True
except:
    print("##BLKWL_ERROR_2 Warning: could not find RACFU, lockdown mode")    
    racfu_enabled = False

class RACFAPI():
    if racfu_enabled:
        #User functions
        def user_exists(self, username: str):
            """Checks if a user exists, returns true or false"""
            result = racfu({"operation": "extract", "admin_type": "user", "profile_name": {username}})
            if result.result["return_codes"]["racf_return_code"] == "0":
                return True
            else:
                return False

        def user_get(self):
            pass

        def user_create(self):
            pass

        def user_delete(self):
            pass

        def user_update(self):
            pass

        #Dataset functions
        def dataset_profile_exists(self):
            """Checks if a dataset profile exists, returns true or false"""
            pass

        def dataset_profile_get(self):
            pass

        def dataset_profile_create(self):
            pass

        def dataset_profile_delete(self):
            pass

        def dataset_profile_update(self):
            pass

        #General resource profile function
        def resource_profile_exists(self):
            """Checks if a general resource profile exists, returns true or false"""
            pass

        def resource_profile_get(self):
            pass

        def resource_profile_create(self):
            pass

        def resource_profile_delete(self):
            pass

        def resource_profile_update(self):
            pass