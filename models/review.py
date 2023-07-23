#!/usr/bin/python3
"""Documentation for the Review Class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """Defines Review Class"""
    place_id = ""
    user_id = ""
    text = ""
