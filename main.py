import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import urllib
import logging
import json


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Thesis(ndb.Model):
	year= ndb.StringProperty(indexed=True)
	title1= ndb.StringProperty(indexed=True)
	abstract= ndb.StringProperty(indexed=True)
	adviser= ndb.StringProperty(indexed=True)
	section= ndb.StringProperty(indexed=True)

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render())

class thesisAPI(webapp2.RequestHandler):
    def get(self):  
        allthesis = Thesis.query().order(-Thesis.year).fetch()
        thesis_list = []

        for thesis in allthesis:
           thesis_list.append({
                # 'id': thesis.key.urlsafe(),
                'year': thesis.year,
                'title1': thesis.title1,
                'abstract': thesis.abstract,
                'adviser': thesis.adviser,
                'section': thesis.section
                })

        response = {
            'result': 'OK',
            'data': thesis_list
        }                           
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self): 
        thesis = Thesis()                               
        thesis.year = self.request.get('year')
        thesis.title1 = self.request.get('title1')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
       	thesis.section = self.request.get('section')
        thesis.put() #returns the key of the entity created
        
        self.response.headers['Content-Type'] = 'application/json'
        response = {
	        'result': 'OK',
	        'data': {
	            # 'id': thesis.key.urlsafe(),
                'year': thesis.year,
                'title1': thesis.title1,
                'abstract': thesis.abstract,
                'adviser': thesis.adviser,
                'section': thesis.section
            }
        }
        self.response.out.write(json.dumps(response))

app = webapp2.WSGIApplication([
    ('/api/thesis', thesisAPI),
    ('/home', MainPageHandler),
    ('/', MainPageHandler)
    
], debug=True)
