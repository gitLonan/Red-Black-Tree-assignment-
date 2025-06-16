from flask import jsonify, request, flash
from app import app, db
import sqlalchemy as sa
from app.models import Building, EstateType, CityPart, City

def init_routes(bp_property_search):

    @bp_property_search.route('/property/search', methods=["GET"])
    def property_search():
        property_type = request.args.get("property_type", type=str)
        min_sq_footage = request.args.get("min_sq_footage",type=float)
        max_sq_footage = request.args.get("max_sq_footage", type=float)
        parking = request.args.get("parking", type=str)
        state = request.args.get("state", type=str)
        estate_type = request.args.get("estate_type", type=str)

        query = db.session.query(Building).join(Building.city_part).join(CityPart.city).join(Building.estate_type)

        if property_type is not None:
            query = query.filter(Building.estate_type.has(EstateType.name.ilike(property_type)))

        if min_sq_footage is not None:
            query = query.filter(Building.square_footage >= min_sq_footage)

        if max_sq_footage is not None:
            query = query.filter(Building.square_footage <= max_sq_footage)

        if parking is not None:
            if parking.lower() == "yes":
                query = query.filter(Building.parking.is_(True))
            elif parking.lower() == "no":
                query = query.filter(Building.parking.is_(False))

        if state:
            query = query.filter(City.name == state)

        if estate_type is not None:
            query = query.filter(Building.estate_type.has(EstateType.name.ilike(estate_type)))

        results = query.all()
        return [b.to_dict() for b in results], 200