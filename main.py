from app import app, db, queues
from models import *
from views  import *
import atexit

#builds queues from DB on start
def build_queues():
	for loc in Location.select():
		print 'building ' + loc.name + ' queue'
		queues[loc.name] = Queue()

	for unproc_cust in Customer.select().where(Customer.checkout == None).order_by(Customer.checkin.asc()):
		print 'adding cust '  + str(unproc_cust.id) + ' to queue ' + unproc_cust.location.name + ' with num ' + str(unproc_cust.number)
		queues[unproc_cust.location.name].put(unproc_cust)


def closedb():
	db.close()
	print 'closed db!'

#connects to DB and init tables if not present
def initialize_db():
	db.connect() #connect to db
	#print 'opened db!'
	db.create_tables([Location, Customer], safe = True) #create tables if not present
	build_queues() #build the queue
	atexit.register(closedb) #register exit handler to close db on exit
	
if __name__ == '__main__':
	initialize_db()
	app.run(
		host = "0.0.0.0",
		port = 8080,
		threaded = True,
		debug = True # MUST BE FALSE FOR DEPLOYMENT!!!
	)
	