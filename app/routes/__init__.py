from flask import Blueprint


def property_retrieval() -> Blueprint:
    bp_property_retrieval = Blueprint("property_retrieval", __name__)
    from .property_retrieval import init_property_retrieval
    init_property_retrieval(bp_property_retrieval)
    return bp_property_retrieval

def property_search_bp() -> Blueprint:
    bp_property_search = Blueprint("property_search", __name__)
    from .property_search import init_property_search
    init_property_search(bp_property_search)
    return bp_property_search

def property_management_bp() -> Blueprint:
    bp_property_management = Blueprint("property_management", __name__)
    from .property_management import init_property_management
    init_property_management(bp_property_management)
    return bp_property_management

def JWT_auth_bp() -> Blueprint:
    bp_jwt_auth = Blueprint("jwt_auth", __name__)
    from .JWT_auth import init_JWT_auth
    init_JWT_auth(bp_jwt_auth)
    return bp_jwt_auth
