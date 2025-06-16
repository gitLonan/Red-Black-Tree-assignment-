from flask import Blueprint


def property_retrieval() -> Blueprint:
    bp_property_retrieval = Blueprint("property_retrieval", __name__)
    from .property_search import init_routes
    init_routes(bp_property_retrieval)
    return bp_property_retrieval

def property_search_bp() -> Blueprint:
    bp_property_search = Blueprint("property_search", __name__)
    from .property_search import init_routes
    init_routes(bp_property_search)
    return bp_property_search

def property_management_bp() -> Blueprint:
    bp_property_management = Blueprint("property_management", __name__)
    from .property_management import init_routes
    init_routes(bp_property_management)
    return bp_property_management
