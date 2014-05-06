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

#_____________________________________________________________
@route('/v1/pins', method = 'GET')
def get_all_pins():
   pins={}
   pins = retrieve_all_pins()
   return str(pins)
###
@route('/v1/boards', method = 'GET')
def get_all_boards():
   boards = {}
   boards = retrieve_all_boards()
   return str(boards)
###
@route('/v1/boards/:board_id', method='GET')
def get_board(board_id):
   board = None
   board = retrieve_board(board_id) 
   return str(board)
###
@route('/v1/pins/:pin_id', method = 'GET')
def get_pin(pin_id):
   pin = None
   pin = retrieve_pin(pin_id)
###   
@route('/v1/reg' , method = 'POST')
#def register():
   


###

@route('/v1/login', method = 'POST')
#def login():
#   login


####
#after login
@route('/v1/user/:user_id' , method = 'GET')
def get_userboards(user_id):
   uboards = {}
   uboards = retrieve_userboards(user_id)
   return str(uboards)
###


#after login
@route('/v1/user/:user_id/pin/upload', method = 'POST')
#def upload_pin(user_id):
   #upload pin
###



#after login
@route('/v1/user/:user_id/board/' , method = 'POST')
#def create_board(user_id):
#create board
###


#after login
@route('/v1/user/:user_id/board/:board_id' , method = 'PUT')
#def attach_pin(user_id,board_id):
   #attach pin
###



#after login
@route('/v1/user/:user_id/board/:board_id' ,method = 'DELETE')
#def delete_board(user_id,board_id):
#delete board
###


#after login
@route('/v1/user/:user_id/pin/:pin_id', method = 'POST')
#def add_comment(user_id,pin_id):
   #add comment
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
