#!/usr/bin/env python3
"""
Base class for database models.
"""

import uuid
from datetime import datetime


class Base:
    """Base class for all models."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a new instance of the Base class."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def save(self):
        """Simulate saving an object to a database or storage."""
        self.updated_at = datetime.now()
        self.__class__.save_to_file(self)

    def to_dict(self):
        """Convert the instance into a dictionary."""
        return {
            key: (value.isoformat() if isinstance(value, datetime) else value)
            for key, value in self.__dict__.items()
        }

    @classmethod
    def save_to_file(cls, obj):
        """Save the object to a file."""
        filename = f"{cls.__name__}.json"
        try:
            with open(filename, "a") as file:
                file.write(f"{obj.to_dict()}\n")
        except Exception as e:
            print(f"Error saving {cls.__name__}: {e}")

    @classmethod
    def load_from_file(cls):
        """Load objects from a file."""
        filename = f"{cls.__name__}.json"
        objects = []
        try:
            with open(filename, "r") as file:
                for line in file:
                    obj_dict = eval(line.strip())  # Convert string to dictionary
                    objects.append(cls(**obj_dict))
        except FileNotFoundError:
            pass
        return objects

    @classmethod
    def search(cls, filters: dict):
        """Search for objects matching the given filters."""
        objects = cls.load_from_file()
        results = []

        for obj in objects:
            match = True
            for key, value in filters.items():
                if getattr(obj, key, None) != value:
                    match = False
                    break
            if match:
                results.append(obj)

        return results
