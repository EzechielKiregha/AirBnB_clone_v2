#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from models.base_model import BaseModel, Base


class Place(BaseModel, Base):
    """This class defines a Place by various attributes"""

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        metadata = Base.metadata
        place_amenity = Table('place_amenity', metadata,
            Column('place_id', String(60),
                   ForeignKey('places.id'), primary_key=True),
            Column('amenity_id', String(60),
                   ForeignKey('amenities.id'), primary_key=True)
        )
        amenities = relationship("Amenity",
                                 overlaps="Amenity.place_amenities", 
                                 secondary=place_amenity, viewonly=False)

    else:
        @property
        def amenities(self):
            """Getter attribute that returns the list of Amenity instances
            linked to the Place
            """
            from models import storage
            from models.amenity import Amenity
            amenities_list = []
            for amenity_id in self.amenity_ids:
                key = "Amenity." + amenity_id
                amenity = storage.all(Amenity).get(key)
                if amenity:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, obj):
            """Setter attribute that handles appending an Amenity.id to
            the attribute amenity_ids. This method accepts only Amenity
            objects
            """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)

    amenity_ids = []
