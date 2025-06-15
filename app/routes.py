from app import app, db
import sqlalchemy as sa
from app.models import Building, EstateType, CityPart, City
from flask import request


@app.route('/building/<building_id>', methods=["GET"])
def building(building_id):
    """Search the database for the building with <building id>"""
    building = db.first_or_404(sa.select(Building).where(Building.id == building_id))
    return building.to_dict()

@app.route('/property/search', methods=["GET"])
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

    if state is not None:
        query = query.filter(City.name == state)

    if estate_type is not None:
        query = query.filter(Building.estate_type.has(EstateType.name.ilike(estate_type)))

    results = query.all()
    return [b.to_dict() for b in results], 200



@app.route('/property/<property_id>', methods=["PUT"])
def property_update(property_id):
    property = db.session.scalar(sa.select(Building).where(Building.id == property_id))
    if not property:
        return "Property not found", 404
    data = request.get_json()
    if data is None:
        return "Error, wrong data type, should be JSON", 400
    
    column_names = [column.key for column in sa.inspect(Building).mapper.column_attrs]

    old_data = {f"{attr}": getattr(property, attr) for attr in data if attr in column_names}
    print(f"Data before updating: {old_data}")

    for key in data:
        if key in column_names:
            setattr(property, key, data[key])

    db.session.commit()
    print(f"Data after updating: {data}")
    return property.to_dict(), 200
