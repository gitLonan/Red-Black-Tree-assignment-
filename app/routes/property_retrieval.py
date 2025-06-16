from flask import jsonify, request, flash
from app import app, db
import sqlalchemy as sa
from app.models import Building, EstateType, CityPart, City



def init_routes(bp_property_retrieval):


    @bp_property_retrieval.route('/building/<building_id>', methods=["POST", "GET"])
    def building(building_id):
        """Search the database for the building with <building id>"""
        if type(building_id) != int:
            return flash("Building ID should be a type int")
        building = db.first_or_404(sa.select(Building).where(Building.id == building_id))
        return building.to_dict()