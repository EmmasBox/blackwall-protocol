
from enum import Enum

from blackwall.api.dataset import dataset_profile_exists, get_dataset_profile
from blackwall.api.group import get_group, group_exists
from blackwall.api.resource import get_resource_profile, resource_profile_exists
from blackwall.api.setropts import get_active_classes
from blackwall.api.user import get_user, user_exists


class QueryType(Enum):
    User = "user"
    Group = "group"
    Dataset = "dataset"
    Resource = "resource"

    @classmethod
    def all(cls) -> set["QueryType"]:
        return {QueryType.User,QueryType.Group,QueryType.Dataset,QueryType.Resource}

def is_id(query: str):
    return len(query) <= 8 and query.isalnum()

def search_user(query: str) -> dict | None:
    if is_id(query) and user_exists(query):
        return get_user(query)
        
def search_group(query: str) -> dict | None:
    if is_id(query) and group_exists(query):
        return get_group(query)

def search_dataset(query: str) -> dict | None:
    if dataset_profile_exists(query):
        return get_dataset_profile(query)

def search_resource(query: str, class_name: str | None) -> dict | None:
    if class_name is str:
        if resource_profile_exists(resource=query,resource_class=class_name):
            return get_resource_profile(resource=query,resource_class=class_name)
    else:
        active_classes = get_active_classes()
        for r_class in active_classes:
            if resource_profile_exists(resource=query,resource_class=r_class):
                return get_resource_profile(resource=query,resource_class=r_class)

def search_database_query_one(query: str, query_types: set[QueryType], class_name: str | None = None):
    results = {}
    for query_type in query_types:
        if query_type is QueryType.User:
            results[query_type] = search_user(query)
        elif query_type is QueryType.Group:
            results[query_type] = search_group(query)
        elif query_type is QueryType.Dataset:
            results[query_type] = search_dataset(query)
        elif query_type is QueryType.Resource:
            results[query_type] = search_resource(query,class_name)
    
    return results

def search_database_query_multiple(query: str, query_types: set[QueryType], class_name: str | None = None):
    pass
