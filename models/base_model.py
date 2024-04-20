#!/usr/bin/python3

"""
Defines the BaseModel class
which serves as the base class for all other classes
"""

import models
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, DateTime
import uuid

Base = declarative_base()


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the BaseModel class"""
        if kwargs:
            self.id = kwargs.get('id', str(uuid.uuid4()))  # Gen unique ID
            self.created_at = datetime.utcnow()  # creation date/time
            self.updated_at = datetime.utcnow()  # last update date/time
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)  # adds attributes from kwargs
            models.storage.new(self)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()
            models.storage.new(self)

    def save(self):
        """Updates the updated_at attribute with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete(self)

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance"""
        new_dict = dict(self.__dict__)
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at
        new_dict['updated_at'] = self.updated_at
        new_dict.pop('_sa_instance_state', None)
        return new_dict

    def __str__(self):
        """Returns a string representation of the instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.to_dict()}"

    @classmethod
    def all(cls):
        """Retrieve all current instances of cls"""
        return models.storage.find_all(cls.__name__)

    @classmethod
    def count(cls):
        """Get the number of all current instances of cls"""
        return len(models.storage.find_all(cls.__name__))

    @classmethod
    def create(cls, *args, **kwargs):
        """Creates an Instance"""
        new = cls(*args, **kwargs)
        return new.id

    @classmethod
    def show(cls, instance_id):
        """Retrieve an instance"""
        return models.storage.find_by_id(cls.__name__, instance_id)

    @classmethod
    def destroy(cls, instance_id):
        """Deletes an instance"""
        return models.storage.delete_by_id(cls.__name__, instance_id)

    @classmethod
    def update(cls, instance_id, *args):
        """Updates an instance"""
        if not args:
            print("** attribute name missing **")
            return
        if len(args) == 1 and isinstance(args[0], dict):
            args = args[0].items()
        else:
            args = [args[:2]]
        for key, value in args:
            models.storage.update_one(cls.__name__, instance_id, key, value)
