from peewee import *
from app import db

#define base model
class BaseModel(Model):
	class Meta:
		database = db

class Location(BaseModel):
	name = CharField(unique = True)
	curr_number = IntegerField()
	high_number = IntegerField()

#define Customer DB obj
class Customer(BaseModel):
	location = ForeignKeyField(Location, related_name = 'customers')
	number = IntegerField()
	checkin = DateTimeField()
	checkout = DateTimeField(null = True)