#!/usr/bin/python3
"""Module documentation for the User Class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Defines the Class User"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
