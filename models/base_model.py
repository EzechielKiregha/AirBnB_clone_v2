#!/usr/bin/python3

"""
Defines the BaseModel class which is the BaseClass
that serves for parents to other classes
"""

from json import dumps
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """Base class for all our classes"""

    def __init__(self, *args, **kwargs):
        """Deserialize and serialize a class"""
        if kwargs:
            self.id = kwargs.get('id', str(uuid4()))  # Generate a unique ID
            self.created_at = datetime.now()  # Set the creation date/time
            self.updated_at = datetime.now()  # Set the last update date/time
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)  # adds attributes from kwargs
            models.storage.new(self)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)

    #     if not kwargs:
    #         self.id = str(uuid4())
    #         self.created_at = datetime.utcnow()
    #         self.updated_at = datetime.utcnow()
    #         models.storage.new(self)
    #     else:
    #         self.id = kwargs.get('id', str(uuid4()))
    #         self.created_at = self.parse_datetime(kwargs['created_at'])
    #         self.updated_at = self.parse_datetime(kwargs['updated_at'])

    # def parse_datetime(self, datetime_str):
    #     return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f')

    def __str__(self):
        """Override str representation of self"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates last updated variable"""
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary representation of self"""
        return {
        **{key: v for key,
           v in self.__dict__.items() if not key.startswith("__")},
        '__class__': type(self).__name__,
        "created_at": (
            self.created_at.isoformat()
            if isinstance(self.created_at, datetime) else self.created_at
        ),
        "updated_at": (
            self.updated_at.isoformat()
            if isinstance(self.updated_at, datetime) else self.updated_at
        ),
    }

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
