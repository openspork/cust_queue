from peewee import *
from datetime import datetime
from app import db

#define base model
class BaseModel(Model):
	class Meta:
		database = db

class Location(BaseModel):
	name = CharField(unique = True)

#define Customer DB obj
class Customer(BaseModel):
	location = ForeignKeyField(Location, related_name = 'customers')
	number = IntegerField()
	checkin = TimeField()
	checkout = TimeField(null = True)