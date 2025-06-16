from flask import jsonify, request, flash
from app import app, db
import sqlalchemy as sa
from app.models import Building, EstateType, CityPart, City
from flask_jwt_extended import jwt_required


def init_property_management(bp_property_management):


    @bp_property_management.route('/property/management', methods=["POST", "GET"])
    @jwt_required()
    def property_management():
        column_names = [column.key for column in sa.inspect(Building).mapper.column_attrs if column.key != 'id']
        print(column_names)
        num_columns = len(column_names)
        print(num_columns)

        data = request.get_json()
        if data is None:
            return jsonify({"Error": "missing data"}), 400
        
        print(f"This is len of data, {len(data)}")
        
        if len(data) < len(column_names):
            print("Some fields need input", 400)
        
        invalid_fields = [field for field in data if field not in column_names]
        print("THESE ARE ERRORS", invalid_fields)
        if len(invalid_fields) > 0:
            return jsonify({"Error": "Fields that dont match with the database: ",
                           "fileds": {invalid_fields}})
        
        try:
            building = Building(**data)
            db.session.add(building)
            db.session.commit()
            return jsonify(building.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"Error": str(e)}), 500
        

    @bp_property_management.route('/property/<property_id>', methods=["PUT"])
    @jwt_required()
    def property_update(property_id):
        property = db.session.scalar(sa.select(Building).where(Building.id == property_id))
        if not property:
            return jsonify({"Error": "Property not found"}), 404
        data = request.get_json()
        if data is None:
            return jsonify({"Error": "wrong data type, should be JSON"}), 400
        
        column_names = [column.key for column in sa.inspect(Building).mapper.column_attrs]
        print(len(column_names))
        old_data = {f"{attr}": getattr(property, attr) for attr in data if attr in column_names}
        print(f"Data before updating: {old_data}")

        for key in data:
            if key in column_names:
                setattr(property, key, data[key])

        db.session.commit()
        print(f"Data after updating: {data}")
        return jsonify(property.to_dict()), 200