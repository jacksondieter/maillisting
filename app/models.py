from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug import generate_password_hash, check_password_hash
import datetime

# app = Flask(__name__)
# app.config.from_pyfile('config.py')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(app)

db = SQLAlchemy()

class Users(db.Model):
  user_id = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(250))
  
  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
    
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)

  def is_authenticated(self):
      return True

  def is_active(self):
      return True

  def is_anonymous(self):
      return False

  def get_id(self):
      return unicode(self.id)

  def __repr__(self):
      return '<User %r>' % (self.username)	

class Campaign(db.Model):
	campaign_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'))
	
	def __init__(self, name, user_id, list_id=None):
		self.name = name
		self.user_id = user_id
		self.list_id = list_id
	
	def __repr__(self):
		return '<Campaign %r>' % self.name

class Products(db.Model):
	product_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True)
	url = db.Column(db.String(80), unique=True)
	campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.campaign_id'))
	
	def __init__(self, name, url, campaign_id):
		self.name = name
		self.url = url
		self.campaign_id = campaign_id
		
	
	def __repr__(self):
		return '<Products %r>' % self.name

class Templates(db.Model):
	template_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), unique=True)
	subject = db.Column(db.String(80))
	sender_name = db.Column(db.String(20))
	sender_email = db.Column(db.String(50))
	html = db.Column(db.Text, unique=True)
	txt = db.Column(db.Text, unique=True)
	campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.campaign_id'))
	product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	
	
	def __init__(self, name, subject, sender_name, sender_email, html, txt, user_id, campaign_id=None, product_id=None):		
		self.subject = subject
		self.name = name
		self.sender_name = sender_name
		self.sender_email = sender_email
		self.html = html
		self.txt = txt
		self.campaign_id = campaign_id
		self.product_id = product_id
		self.user_id = user_id
		
	def __repr__(self):
		return '<Templates %r>' % self.name	

class Lists(db.Model):
	list_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True)
	emails = db.relationship('Email', backref='lists', lazy='dynamic')
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	
	def __init__(self, name,user_id):
		self.name = name
		self.user_id = user_id
		
	def __repr__(self):
		return '<Mail List %r>' % self.name

class Email(db.Model):
	email_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	email = db.Column(db.String(50))
	list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'))
	pixels = db.relationship('Trackemail', backref='email', lazy='dynamic')
	
	def __init__(self, email, list_id, name=''):
		self.name = name
		self.email = email
		self.list_id = list_id

	def __repr__(self):
		return '<Email %r>' % self.email

class Trackemail(db.Model):
	trackemail_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.campaign_id'))
	email_id = db.Column(db.Integer, db.ForeignKey('email.email_id'))
	date_email = db.Column(db.DateTime, default=datetime.datetime.utcnow())
	tracklink = db.relationship('Tracklink', backref='trackemail', lazy='dynamic')
	
	
	def __init__(self,user_id, campaign_id, email_id):
		self.user_id = user_id
		self.campaign_id = campaign_id
		self.email_id = email_id

class Tracklink(db.Model):
	tracklink_id = db.Column(db.Integer, primary_key=True)
	trackemail_id = db.Column(db.Integer, db.ForeignKey('trackemail.trackemail_id'))
	product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
	date_link = db.Column(db.DateTime, default=datetime.datetime.utcnow())
	
	def __init__(self, trackemail_id, product_id):
		self.trackemail_id = trackemail_id
		self.product_id = product_id

def main():
	db.create_all()

			
if __name__ == "__main__":
	main()
