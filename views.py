from flask import Flask, render_template, url_for, redirect, send_file
from app import app, queues
from models import Location, Customer
from datetime import date, datetime
from Queue import Queue

@app.route('/<string:loc_name>/')
def stream(loc_name):
	return 'Stream for: ' + loc_name + ', queue at ' + str(Location.get(Location.name == loc_name).curr_number)

@app.route('/dash/')
def dash():
	return 'todo'

@app.route('/<string:loc_name>/new_cust/')
def new_cust(loc_name):
	print 'new cust ' + loc_name
	try:
		location = Location.get(Location.name == loc_name) #get location if exists
	except Location.DoesNotExist:
		location = Location.create(name = loc_name, curr_number = 0, high_number = 0) #create location if not
		queues[location.name] = Queue() #create new queue for location
		pass
	location.high_number += 1 #increment location's high number
	location.save() #write to database
	#add new customer to queue
	queues[location.name].put(Customer.create(location = location,
												number = location.high_number, 
												checkin = datetime.now()))
	return 'Adding cust at ' + location.name + ' with num ' + str(location.high_number)

@app.route('/<string:loc_name>/next_cust/')
def next_cust(loc_name):
	if not queues[loc_name].empty():
		location = Location.get(Location.name == loc_name) #get location
		curr_cust = queues[location.name].get() #get customer from location's queue
		curr_cust.checkout = datetime.now() #set queue checkout time
		curr_cust.save() #save finished cust to database
		location.curr_number = curr_cust.number #increment location's number to next cust
		location.save() #save location to database
		return 'cust with num ' + str(curr_cust.number) + ' waited ' + str((curr_cust.checkout - curr_cust.checkin).total_seconds()) + ' seconds.'
	else:
		return 'no current customer, please try again when customers are waiting'

	