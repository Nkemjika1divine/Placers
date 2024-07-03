#!/usr/bin/python3
"""The BaseModel Module"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base
from typing import Dict, List, TypeVar
from uuid import uuid4


Base = declarative_base()


class BaseModel:
    """The BaseModel class"""
    __abstract__ = True
    id = Column(String(50), primary_key=True, nullable=False)
    time_created = Column(DateTime, default=datetime.now, nullable=False)
    time_updated = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """Initializing the Basemodel class"""
        if 'id' not in kwargs:
            self.id = str(uuid4())
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                elif key == 'time_created' or key == 'time_updated':
                    setattr(self, key, datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, value)
        else:
            self.time_created = datetime.now()
            self.time_updated = datetime.now()
    
    def to_dict(self) -> Dict[str, any]:
        """Returns a dictionary representation of the object"""
        copy = self.__dict__.copy()
        copy['__class__'] = self.__class__.__name__
        if 'time_created' in copy:
            copy['time_created'] = self.time_created.isoformat()
        if 'time_updated' in copy:
            copy['time_updated'] = self.time_updated.isoformat()
        if "_sa_instance_state" in copy:
            del copy["_sa_instance_state"]
        return copy
    
    def __str__(self) -> str:
        """Returns a string representation of the object"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def save(self) -> None:
        """Saves a new object"""
        from models import storage
        self.time_updated = datetime.now()
        storage.new(self)
        storage.save()
    
    def delete(self) -> None:
        from models import storage
        """delete the current instance from the storage"""
        storage.delete(self)
    
    @classmethod
    def search(cls, key_values: dict = {}) -> List[TypeVar('BaseModel')]:
        """Searches and returns all objects with matching attributes"""
        from models import storage
        class_name = cls.__name__
        all_data = storage.all(class_name)
        class_list = []
        if len(key_values) == 0:
            if all_data:
                for key, value in all_data.items():
                    class_list.append(value)
                return class_list
        for key, value in key_values.items():
            print("checking attribute of key")
            print(f"{cls} {type(key)} {value}")
            getattr_val = getattr(cls, key, "unknown")
            print(getattr_val)
            if getattr_val == value:
                print("attribute of key = value")
                if all_data:
                    for x, y in all_data.items():
                        for m, n in y.__dict__.items():
                            if m == key:
                                if getattr(cls, n) == value:
                                    class_list.append(y)
        return class_list
                
        
