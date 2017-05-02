from flask import Flask, render_template, url_for, redirect, send_file
from app import app, queues
from models import Location, Customer
from datetime import datetime
from Queue import Queue

@app.route('/<loc>/')
def stream(loc):
	return 'Stream for: ' + loc

@app.route('/<loc_name>/new_cust/')
def new_cust(loc_name):
	try:
		location = Location.get(Location.name == loc_name) #get location
	except Location.DoesNotExist: 
		location = Location.create(name = loc_name) #create location
		queues[location.name] = Queue() #create new queue
	#add new customer to queue
	queues[location.name].put(Customer.create(location = location, checkin = datetime.now().time()))
	return 'Adding cust at ' + loc_name

@app.route('/<loc_name>/next_cust/')
def next_cust(loc_name):
	location = Location.get(Location.name == loc_name)
	curr_cust = queues[location.name].get()
	curr_cust.checkout = datetime.now().time()
	curr_cust.save()
	return str(curr_cust.id) + str(curr_cust.checkin) + str(curr_cust.checkout)



	