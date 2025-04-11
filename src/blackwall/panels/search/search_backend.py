
from blackwall.api.user import user_exists, get_user
from blackwall.api.dataset import dataset_profile_exists, get_dataset_profile
from blackwall.api.resource import resource_profile_exists, get_resource_profile
from blackwall.api.setropts import get_active_classes

def user_possible(query: str):
    return len(query) <= 8 and query.isalnum()

def search_user(query: str):
    if user_possible(query):
        if user_exists(query):
            return get_user(query)

def search_dataset(query: str):
    if dataset_profile_exists(query):
        return get_dataset_profile(query)

def search_resource(query: str, class_name: str | None):
    if class_name is str:
        if resource_profile_exists(resource=query,resource_class=class_name):
            return get_resource_profile(resource=query,resource_class=class_name)
    else:
        active_classes = get_active_classes()
        for r_class in active_classes:
            if resource_profile_exists(resource=query,resource_class=r_class):
                return get_resource_profile(resource=query,resource_class=r_class)

def search_database_query_one(query: str, class_name: str, query_type: str):
    if query_type == "any":
        user_result = search_user(query)
        dataset_result = search_dataset(query)
        resource_result = search_resource(query,class_name=None)
    elif query_type == "user":
        user_result = search_user(query)
    elif query_type == "dataset":
        dataset_result = search_dataset(query)
    elif query_type == "resource":
        resource_result = search_resource(query,class_name)

def search_database_query_multiple(query: str, query_type: str):
    if query_type == "any":
        pass
