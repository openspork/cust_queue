from peewee import *
from Queue import Queue
from datetime import datetime
import atexit

#define database
database = SqliteDatabase('customers.db')

#define base model
class BaseModel(Model):
	class Meta:
		database = database

#define Customer DB obj
class Customer(BaseModel):
	id = PrimaryKeyField(null = False, unique = True)
	checkin = TimeField(null = False)
	checkout = TimeField(null = True)

def closedb():
	database.close()
	print 'closed db!'

#connects to DB and init tables if not present
def initialize_db():
	database.connect() #connect to db
	database.create_tables([Customer], safe=True) #safe -- will not override if existing
	atexit.register(closedb) #registers exit handler to close db

def initialize_q():
	print 'UNPROCESSED:'
	for unproc_cust in Customer.select().where(Customer.checkout == None).order_by(Customer.checkin.asc()):
		print 'adding cust' + str(unproc_cust.id) + ' to queue'
		q.put(unproc_cust)

#inits db
initialize_db()

#initilize queue
q = Queue()
initialize_q()

print 'loaded'

#creates a new db entry and adds to queue
def new_customer():
	q.put(Customer.create(checkin = datetime.now().time()))

def next_customer():
	cust = q.get()
	cust.checkout = datetime.now().time()
	cust.save()
	print cust.id, cust.checkin, cust.checkout



