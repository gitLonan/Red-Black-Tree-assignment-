from app import db
from typing import Optional
import sqlalchemy as sa     
import sqlalchemy.orm as so 

from datetime import datetime, timezone


class Building(db.Model):
    __tablename__ = "building"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, nullable=False)
    square_footage: so.Mapped[float] = so.mapped_column(sa.Float, index=True)
    construction_year: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    land_area: so.Mapped[float] = so.mapped_column(sa.Float, index=True)
    registration: so.Mapped[bool] = so.mapped_column(sa.Boolean, index=True)
    rooms: so.Mapped[float] = so.mapped_column(sa.FLOAT, index=True)
    bathrooms: so.Mapped[float] = so.mapped_column(sa.Integer, index=True)
    parking: so.Mapped[bool] = so.mapped_column(sa.Boolean, index=True)
    price: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    #relationship
    building_heating: so.WriteOnlyMapped[list["BuildingHeating"]] = so.relationship(back_populates="building")
    building_amenity: so.WriteOnlyMapped[list["BuildingAmenity"]] = so.relationship(back_populates="building")
    building_floor: so.WriteOnlyMapped[list["BuildingFloor"]] = so.relationship(back_populates="building")
    city_part: so.Mapped["CityPart"] = so.relationship(back_populates="building")
    estate_type: so.Mapped["EstateType"] = so.relationship(back_populates="building")
    offer: so.Mapped["Offer"] = so.relationship(back_populates="building")
    #FOREIGN KEYS
    estate_type_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("estate_type.id"))
    offer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("offer.id"))
    city_part_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("city_part.id"))
    

class BuildingAmenity(db.Model):
    __tablename__ = "building_amenity"

    #relationship
    building: so.Mapped["Building"] = so.relationship(back_populates="building_amenity")
    amenity: so.Mapped["Amenity"] = so.relationship(back_populates="building_amenity")
    #FOREIGN KEYS
    building_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("building.id"), nullable=False, primary_key=True)
    amenity_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("amenity.id"), nullable=False, primary_key=True)

class Amenity(db.Model):
    __tablename__ = "amenity"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[int] = so.mapped_column(sa.String, nullable=False)
    #relationship
    building_amenity: so.WriteOnlyMapped[list["BuildingAmenity"]] = so.relationship(back_populates="amenity")



class BuildingFloor(db.Model):
    __tablename__ = "building_floor"

    floor_level: so.Mapped[str] = so.mapped_column(sa.String)
    floor_total: so.Mapped[str] = so.mapped_column(sa.Integer)
    #relationship
    building: so.Mapped["Building"] = so.relationship(back_populates="building_floor")
    #FOREIGN KEYS
    building_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("building.id"), nullable=False, primary_key=True)



class BuildingHeating(db.Model):
    __tablename__ = "building_heating"
    
    #relationship
    heating: so.Mapped["Heating"] = so.relationship(back_populates="building_heating")
    building: so.Mapped["Building"] = so.relationship(back_populates="building_heating")
    #FOREIGN KEYS
    heating_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("heating.id"), nullable=False, primary_key=True)
    building_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("building.id"), nullable=False, primary_key=True)

class Heating(db.Model):
    __tablename__ = "heating"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    #relationship
    building_heating: so.WriteOnlyMapped[list["BuildingHeating"]] = so.relationship(back_populates="heating")



class City(db.Model):
    __tablename__ = "city"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    #relationship
    city_parts: so.WriteOnlyMapped[list["CityPart"]] = so.relationship(back_populates="city")
    state: so.Mapped["State"] = so.relationship(back_populates="city")
    #FOREIGN KEYS
    
class CityPart(db.Model):
    __tablename__ = "city_part"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    #relationship
    city: so.Mapped["City"] = so.relationship(back_populates="city_parts")
    building: so.WriteOnlyMapped[list["Building"]] = so.relationship(back_populates="city_part")
    #FOREIGN KEY
    city_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("city.id"))

class State(db.Model):
    __tablename__ = "state"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.MappedColumn[str] = so.mapped_column(sa.String, nullable=False)
    #relationship
    city: so.WriteOnlyMapped[list["City"]] = so.relationship(back_populates="state")



class EstateType(db.Model):
    __tablename__ = "estate_type"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
    #relationship
    building: so.WriteOnlyMapped[list["Building"]] = so.relationship(back_populates="estate_type")



class Offer(db.Model):
    __tablename__ = "offer"


    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String, nullable=False)
     #relationship
    building: so.WriteOnlyMapped[list["Building"]] = so.relationship(back_populates="offer")
