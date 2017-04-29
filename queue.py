from peewee import *
from Queue import Queue
from datetime import datetime

##############################################################################
#SETUP DB
##############################################################################

#define database
database = SqliteDatabase('customers.db')
#create customer queue
q = Queue()

#define base model
class BaseModel(Model):
	class Meta:
		database = database

#define Customer DB obj
class Customer(BaseModel):
	id = PrimaryKeyField(null = False, unique = True)
	checkin = TimeField(null = False)
	checkout = TimeField(null = True)
	agent = CharField(null = True)

#define Counter DB obj
class Counter(BaseModel):
	id = PrimaryKeyField(null = False, unique = True)
	isBusy = BooleanField(null = False)

#connects to DB and init tables if not present
def initialize_db():
	database.connect() #connect to db
	database.create_tables([Customer], safe=True) #safe -- will not override

#inits db
initialize_db()

#creates a new db entry and adds to queue
def new_ticket():
	q.put_nowait(Customer.create(checkin = datetime.now().time()))

def open_ticket():
	print 'opening ticket'

def close_ticket():
	print q.get().id

counter = Counter()

print counter.isBusy



''''
for cust in Customer.select():
	print cust.id, cust.checkin
'''

