#!/usr/bin/python3
"""The Database Module"""
from dotenv import load_dotenv
from models.basemodel import Base
from os import environ
from sqlalchemy import create_engine


load_dotenv()


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