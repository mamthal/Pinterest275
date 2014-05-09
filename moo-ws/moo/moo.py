"""
6, Apr 2013

Example bottle (python) RESTful web service.

This example provides a basic setup of a RESTful service

Notes
1. example should perform better content negotiation. A solution is
   to use minerender (https://github.com/martinblech/mimerender)
"""
import time
import sys
import socket
import string
import random
import json
import couchdb
# bottle framework
from bottle import request, response, route, run, template

# moo
from classroom import Room

# virtual classroom implementation
room = None

def setup(base,conf_fn):
   print '\n**** service initialization ****\n'
   global room 
   room = Room(base,conf_fn)

#
# setup the configuration for our service

@route('/')
def root():
   print "--> root"
   return 'welcome'

#Pins are public. List all pins of all users. 
@route('/v1/pins', method = 'GET')
def get_all_pins():
		
	rsp=[]
	
	couch=couchdb.Server()
	db=couch['pinterester']
	
	for dbObj in db:
		print dbObj
		doc=db[dbObj]
		#print doc
		newvar = doc['Pins']
		for i in range(len(newvar)):
			onepin= newvar[i]
			rsp.append(onepin)
	return json.dumps(rsp)


###
@route('/v1/boards', method = 'GET')
def get_all_boards():
   	boards = []
	couch=couchdb.Server()
	db=couch['pinterester']
	
	for dbObj in db:
		print dbObj
		doc=db[dbObj]
		#print doc
		newvar = doc['Boards']
		for i in range(len(newvar)):
			oneboard= newvar[i]
			boards.append(oneboard)
	return json.dumps(boards)

   
###
@route('/v1/boards/:board_id', method='GET')
def get_board(board_id):
   #board = None
   #board = retrieve_board(board_id) 
	rsp = []
	print "Requesting for board_id = " + board_id
	new_board_id= board_id.strip(':')
	print new_board_id
	couch = couchdb.Server()
	db = couch['pinterester']
	for dbObj in db:
		#print dbObj
		doc = db[dbObj]
		newvar = doc['Boards']
		for i in range(len(newvar)):
			oneboard=newvar[i]
			#print oneboard
			match = oneboard.get('board_id')
			if new_board_id == match:
				print oneboard.values()
				rsp.append(oneboard)
				return json.dumps(rsp)

	rsp.append("Board ID requested for not found")
	return json.dumps(rsp)
   

#
#function to generate access token

def token_generator(size, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


###
@route('/v1/pin/:pin_id', method = 'GET')
def get_pin(pin_id):
	rsp = []
	print "Requesting for pin_id = " + pin_id
	new_pin_id= pin_id.strip(':')
	print new_pin_id
	couch = couchdb.Server()
	db = couch['pinterester']
	for dbObj in db:
		#print dbObj
		doc = db[dbObj]
		newvar = doc['Pins']
		for i in range(len(newvar)):
			onepin=newvar[i]
			#print oneboard
			match = onepin.get('pin_id')
			if new_pin_id == match:
				print onepin.values()
				rsp.append(onepin)
				return json.dumps(rsp)
	rsp.append("Pin ID requested for not found")
	return json.dumps(rsp)   
###   
@route('/v1/reg' , method = 'POST')
def signup():
	fmt = __format(request)
	print ' format  %s request' %fmt %request	
  	response.content_type = __response_format(fmt)
	accessToken=token_generator(6,"qwedbh34gfh")
     	username = request.json['username']
     	password = request.json['password']
	name = request.json['name']
	#connecting to database
	couch = couchdb.Server()
	db = couch['pinterester']
	doc = {'username': username,"password":password,"name":name,"Boards":[],"Pins":[]}
	db.save(doc)
   	if fmt == Room.html:
      		return '<h2>%s</h2>' %accessToken
		
   	elif fmt == Room.json:
      		rsp = {}
		rsp["userid"]=accessToken
      		return json.dumps(rsp)
   	else:
      		return accessToken
   


###

@route('/v1/login', method = 'POST')
def signin():
	fmt = __format(request)
	print ' format  %s' %fmt	
  	response.content_type = __response_format(fmt)
	accessToken=token_generator(6,"qwedbh34gfh")
	response.content_type = 'application/json'
     	username = request.json['username']
     	password = request.json['password']
	couch = couchdb.Server()
	db = couch['pinterester']
	print db
	for dbobj in db:
   		doc=db[dbobj];
		print doc
        	uValidation=doc['username']
		pValidation=doc['password']	
		if (uValidation == username and pValidation==password):
			if fmt == Room.html:
      				return '<h1>Welcome %s</h1>' % username,'<h2>%s</h2>' %password, '<h2>%s</h2>' %accessToken
		
   			elif fmt == Room.json:
      				rsp = {}
      				rsp["username"] = username
				rsp["password"] = password
				rsp["accessToken"]=accessToken
      				return json.dumps(rsp)		
   			else:
      				return username + password + accessToken
			break
		else:
			print "checking again"
	
	if fmt == Room.html:
      		return '<h1>User Not found</h1>'
		
   	elif fmt == Room.json:
      		rsp = {}
		rsp["error"]="user not found"
      		return json.dumps(rsp)		
   	else:
      		return "user not found"


####
#after login
@route('/v1/user/:user_id' , method = 'GET')
def get_userboards(user_id):
   	uboards = []
	temp = {}
	print "User ID is : " + user_id #name for now
	new_user_id= user_id.strip(':')
	couch = couchdb.Server()
	db = couch['pinterester']
	for dbObj in db:
		#check only that user
		doc = db[dbObj]
		check_name = doc['Name']
		if check_name == new_user_id:
			temp= doc
			name= temp['Name']
			print name
			uboards.append(name)
			myboards = temp['Boards']
			for i in range(len(myboards)):
				print myboards[i]
				uboards.append(myboards[i])
				return json.dumps(uboards)
	uboards.append("Required document not found..")
	return json.dumps(uboards) 
		
   
###


#after login
@route('/v1/user/:user_id/pin/upload', method = 'POST')
def uploadPin(user_id):
	print "user id %s" %user_id
	fmt = __format(request)
	response.content_type=__response_format(fmt)
	url=request.json['client_url']
	couch = couchdb.Server()
	db = couch['pinterester']
	print db
	for dbObj in db:
		doc=db[dbObj]
		uValidation=":"+doc['username']
		if uValidation==user_id:
			pins=doc["Pins"]
			pinId="pin_"+token_generator(3,"abcdef123456")
			pinDict= {'client_url':url,"pin_id":pinId,"Comments":[] }
			pins.append(pinDict)
			db.save(doc)
			rsp = {}
			rsp["pin_id"]=pinId
      			return json.dumps(rsp)	
		
	rsp={}
	rsp["msg"]="user Id is wrong"
	return json.dumps(rsp)



#after login
@route('/v1/user/:user_id/board/' , method = 'POST')
def createBoard(user_id):
	print "user id %s" %user_id
	fmt = __format(request)
	response.content_type=__response_format(fmt)
	boardName=request.json['boardName']
	#boardId=request.json['boardId']
	couch = couchdb.Server()
	db = couch['pinterester']
	print db
	for dbObj in db:
		doc=db[dbObj]
		uValidation=":"+doc['username']
		if uValidation==user_id:
			Boards=doc["Boards"]
			boardId="board_"+token_generator(3,"abcdef123456")
			BoardDict= {'boardName': boardName,"boardId":boardId}
			Boards.append(BoardDict)
			db.save(doc)
			rsp = {}
			rsp["boardId"]=boardId
      			return json.dumps(rsp)	
		
	rsp={}
	rsp["msg"]="user Id is wrong"
	return json.dumps(rsp)


#after login
@route('/v1/user/:user_id/board/:board_id' , method = 'PUT')
def attachPin(user_id,board_id):
	fmt = __format(request)
	rsp={}
	board_id=board_id.strip(":")
	user_id=user_id.strip(":")
	response.content_type =__response_format(fmt)
	newPinId=request.json["pin_id"]
	couch=couchdb.Server()
	db=couch['pinterester']
	for dbObj in db:
		doc=db[dbObj]
		uValidation=doc['username']
		if uValidation == user_id:
			boardsList=doc['Boards']
			for i in range(len(boardsList)):
				boardDict=boardsList[i]
				print boardDict
				print boardDict.has_key("boardId")
				boardId=boardDict.get("boardId")
			
				if boardId == board_id:
					newPin={"pin_id":newPinId}
					boardDict.update(newPin)
					print boardDict
					db.save(doc)
					rsp["success"]="true"
					return json.dumps(rsp)
	rsp["success"]="false"
	return json.dumps(rsp)



#after login
@route('/v1/user/:user_id/board/:board_id' ,method = 'DELETE')
#def delete_board(user_id,board_id):
#delete board
###


#after login
@route('/v1/user/:user_id/pin/:pin_id', method = 'POST')
def add_comment(user_id,pin_id):
	fmt = __format(request)
	rsp={}
       #user_id = user_id.strip(":")
       #pin_id = pin_id.strip(":")
        response.content_type =__response_format(fmt)
        newComment = request.json["comment"]
        couch = couchdb.Server()
	db = couch['pinterester']        
        for dbObj in db:
           doc = db[dbObj]
           uValid = doc["_id"]
           if uValid == user_id:
              pinList = doc["Pins"]
              for pin in pinList:
                 thatPin = pin["pin_id"]
                 if thatPin == pin_id:
                    commentList = pin["Comments"]
                    if commentList is None:
                       commentList = []
                    commentList.append(newComment)
                    pin["Comments"] = commentList
                    db.save(doc)
                    rsp["statuscode"]="200"
		    rsp["success"] = "true"
                    return json.dumps(rsp)
	rsp["statuscode"]="400"
	rsp["success"] = "false"
	return json.dumps(rsp)
                    
              
              
#_________________________________________________________________

#
@route('/moo/ping', method='GET')
def ping():
   return 'ping %s - %s' % (socket.gethostname(),time.ctime())

#
# Development only: echo the configuration of the virtual classroom.
#
# Testing using curl:
# curl -i -H "Accept: application/json" http://localhost:8080/moo/conf
#
# WARN: This method should be disabled or password protected - dev only!
#
@route('/moo/conf', method='GET')
def conf():
   fmt = __format(request)
   response.content_type = __response_format(fmt)
   return room.dump_conf(fmt)

#
# example of a RESTful method. This example is very basic, it does not 
# support much in the way of content negotiation.
#
@route('/moo/echo/:msg')
def echo(msg):
   fmt = __format(request)
   response.content_type = __response_format(fmt)
   if fmt == Room.html:
      return '<h1>%s</h1>' % msg
   elif fmt == Room.json:
      rsp = {}
      rsp["msg"] = msg
      return json.dumps(all)
   else:
      return msg


#
# example of a RESTful query
#
@route('/moo/data/:name', method='GET')
def find(name):
   print '---> moo.find:',name
   return room.find(name)

#
# example adding data using forms
#
@route('/moo/data', method='POST')
def add():
   print '---> moo.add'

   # example list form values
   for k,v in request.forms.allitems():
      print "form:",k,"=",v

   name = request.forms.get(k)
   value = request.forms.get(v)
   return room.add(name,value)

#
# Determine the format to return data (does not support images)
#
# TODO method for Accept-Charset, Accept-Language, Accept-Encoding, 
# Accept-Datetime, etc should also exist
#
def __format(request):
   #for key in sorted(request.headers.iterkeys()):
   #   print "%s=%s" % (key, request.headers[key])

   types = request.headers.get("Accept",'')
   subtypes = types.split(",")
   for st in subtypes:
      sst = st.split(';')
      if sst[0] == "text/html":
         return Room.html
      elif sst[0] == "text/plain":
         return Room.text
      elif sst[0] == "application/json":
         return Room.json
      elif sst[0] == "*/*":
         return Room.json

      # TODO
      # xml: application/xhtml+xml, application/xml
      # image types: image/jpeg, etc

   # default
   return Room.html

#
# The content type on the reply
#
def __response_format(reqfmt):
      if reqfmt == Room.html:
         return "text/html"
      elif reqfmt == Room.text:
         return "text/plain"
      elif reqfmt == Room.json:
         return "application/json"
      else:
         return "*/*"
         
      # TODO
      # xml: application/xhtml+xml, application/xml
      # image types: image/jpeg, etc
