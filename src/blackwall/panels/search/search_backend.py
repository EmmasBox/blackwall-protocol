
from blackwall.api.user import user_exists, user_get
from blackwall.api.dataset import dataset_profile_exists, dataset_profile_get
from blackwall.api.resource import resource_profile_exists, resource_profile_get

def user_possible(query: str):
    return len(query) <= 8 and query.isalnum()

def search_user(query: str):
    if user_possible(query):
        if user_exists(query):
            return user_get(query)

def search_dataset(query: str):
    if dataset_profile_exists(query):
        return dataset_profile_get(query)

def search_resource(query: str):
    if resource_profile_exists(query):
        return resource_profile_get(query)

def search_database_query_one(query: str, query_type: str):
    if query_type == "any":
        user_result = search_user(query)
        dataset_result = search_dataset(query)
        resource_result = search_resource(query)
    elif query_type == "user":
        user_result = user_result = search_user(query)
    elif query_type == "dataset":
        dataset_result = search_dataset(query)
    elif query_type == "resource":
        resource_result = search_resource(query)

def search_database_query_multiple(query: str, query_type: str):
    if query_type == "any":
        pass
