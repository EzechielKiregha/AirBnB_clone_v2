#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
from datetime import datetime
import json

from models.engine.errors import InstanceNotFoundError, ModelNotFoundError


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}
    models = ("BaseModel", "User", "Place", "State\
", "City", "Amenity", "Review")

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return FileStorage.__objects
        return {k: v for k, v in FileStorage.__objects.items() if isinstance(v, cls)}

    # def all(self):
    #     """Returns a dictionary of models currently in storage"""
    #     return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def delete(self, obj=None):
        """Deletes obj from __objects if it exists"""
        if obj is None:
            return
        key = obj.__class__.__name__ + '.' + obj.id
        if key in FileStorage.__objects:
            del FileStorage.__objects[key]

    def reload(self):
        """de-serialize persisted objects"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            deserialized = {}
            with open(FileStorage.__file_path, "r") as f:
                deserialized = json.loads(f.read())
            FileStorage.__objects = {
                key:
                    classes[obj["__class__"]](**obj)
                    # eval(obj["__class__"])(**obj)
                    for key, obj in deserialized.items()}
            
            # for k , v in FileStorage.__objects.items():
            #     print(k, " : ", v)
            
        except (FileNotFoundError, json.JSONDecodeError):
            # No need for error
            pass

    # def reload(self):
    #     """Loads storage dictionary from file"""
    #     from models.base_model import BaseModel
    #     from models.user import User
    #     from models.place import Place
    #     from models.state import State
    #     from models.city import City
    #     from models.amenity import Amenity
    #     from models.review import Review

    #     classes = {
    #                 'BaseModel': BaseModel, 'User': User, 'Place': Place,
    #                 'State': State, 'City': City, 'Amenity': Amenity,
    #                 'Review': Review
    #               }
    #     try:
    #         temp = {}
    #         with open(FileStorage.__file_path, 'r') as f:
    #             temp = json.load(f)
    #             for key, val in temp.items():
    #                     self.all()[key] = classes[val['__class__']](**val)
    #     except FileNotFoundError:
    #         pass

    def find_by_id(self, model, obj_id):
        """Find and return an elemt of model by its id"""
        F = FileStorage
        if model not in F.models:
            # Invalid Model Name
            # Not yet Implemented
            raise ModelNotFoundError(model)

        key = model + "." + obj_id
        if key not in F.__objects:
            # invalid id
            # Not yet Implemented
            raise InstanceNotFoundError(obj_id, model)

        return F.__objects[key]

    def delete_by_id(self, model, obj_id):
        """Find and return an elemt of model by its id"""
        F = FileStorage
        if model not in F.models:
            raise ModelNotFoundError(model)

        key = model + "." + obj_id
        if key not in F.__objects:
            raise InstanceNotFoundError(obj_id, model)

        del F.__objects[key]
        self.save()

    def find_all(self, model=""):
        """Find all instances or instances of model"""
        if model and model not in FileStorage.models:
            raise ModelNotFoundError(model)
        results = []
        for key, val in FileStorage.__objects.items():
            if key.startswith(model):
                results.append(str(val))
        return results

    def update_one(self, model, iid, field, value):
        """Updates an instance"""
        F = FileStorage
        if model not in F.models:
            raise ModelNotFoundError(model)

        key = model + "." + iid
        if key not in F.__objects:
            raise InstanceNotFoundError(iid, model)

        if field in ("id", "updated_at", "created_at"):
            # not allowed to be updated
            return
        inst = F.__objects[key]
        try:
            # if instance has that value
            # cast it to its type
            vtype = type(inst.__dict__[field])
            inst.__dict__[field] = vtype(value)
        except KeyError:
            # instance doesn't has the field
            # assign the value with its type
            inst.__dict__[field] = value
        finally:
            inst.updated_at = datetime.utcnow()
            self.save()
