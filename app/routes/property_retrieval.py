from flask import jsonify, request, flash
from app import app, db
import sqlalchemy as sa
from app.models import Building, EstateType, CityPart, City



def init_property_retrieval(bp_property_retrieval):


    @bp_property_retrieval.route('/building/<building_id>', methods=["POST", "GET"])
    def building(building_id):
        """Search the database for the building with <building id>"""
        try:
            building_id = int(building_id)
        except ValueError:
            return jsonify({"error": "Building ID must be an integer"}), 400
        building = db.first_or_404(sa.select(Building).where(Building.id == building_id))
        return jsonify(building.to_dict()), 200