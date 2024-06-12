#!/usr/bin/python3
"""The BaseModel Module"""
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from uuid import uuid4


class BaseModel:
    """The BaseModel class"""
    __abstract__ = True
    id = Column(String(50), primary_key=True, nullable=False)
    time_created = Column(DateTime, default=datetime.now, nullable=False)
    time_updated = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, *args, **kwargs):
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
    
    def to_dict(self):
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
    
    def __str__(self):
        """Returns a string representation of the object"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)