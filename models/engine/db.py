#!/usr/bin/python3
"""The Database Module"""
from dotenv import load_dotenv
from models.basemodel import Base
from models.place import Place
from models.review import Review
from models.user import User
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Dict

load_dotenv()


classes = {
    "User": User,
    "Place": Place,
    "Review": Review
}


class DB:
    """The Database Class
    - Handles all database operations
    """
    __session = None
    __engine = None

    def __init__(self) -> None:
        """Initializing the Database"""
        PLACERS_DB = environ.get("PLACERS_DB")
        PLACERS_PORT = environ.get("PLACERS_PORT")
        PLACERS_USER = environ.get("PLACERS_USER")
        PLACERS_PWD = environ.get("PLACERS_PWD")
        PLACERS_HOST = environ.get("PLACERS_HOST")
        self.__engine = create_engine(
            "mysql+mysqlconnector://{}:{}@{}:{}/{}".format(PLACERS_USER,
                                                           PLACERS_PWD,
                                                           PLACERS_HOST,
                                                           PLACERS_PORT,
                                                           PLACERS_DB))
        if environ.get("PLACERS_ENV") == "test":
            try:
                Base.metadata.drop_all(self.__engine)
            except Exception:
                print("There is no table in the database")
    
    def all(self, cls=None) -> Dict[str: any]:
        """query on the current database session"""
        result = {}
        if cls is not None:
            for obj in self.__session.query(classes[cls]).all():
                ClassName = obj.__class__.__name__
                keyName = ClassName + "." + obj.id
                result[keyName] = obj
        else:
            for cls in classes.values():
                for obj in self.__session.query(cls).all():
                    class_name = obj.__class__.__name__
                    key = class_name + "." + obj.id
                    result[key] = obj
        return result
    
    def new(self, obj) -> None:
        """add an object to the database"""
        self.__session.add(obj)

    def save(self) -> None:
        """commit all changes of the database"""
        self.__session.commit()

    def delete(self, obj=None) -> None:
        """delete from the database"""
        if obj:
            self.__session.delete(obj)
    
    def reload(self) -> None:
        """reloads from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
    
    def count(self, cls=None) -> int:
        """count the number of objects in storage"""
        from models import storage
        if not cls:
            count = 0
            all_classes = storage.all()
            for i in all_classes:
                count += 1
            return count
        else:
            count = len(storage.all(cls))
        return count