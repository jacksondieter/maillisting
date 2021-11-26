from flask import Flask, request, redirect, url_for, render_template, Blueprint , flash, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from jinja2 import Template
import datetime
from app.models import *

track = Blueprint('track',__name__, static_folder='static', url_prefix='/track')

mail = Mail()
#env = Environment(loader=PackageLoader('my_app', 'templates'))

@track.route('/track', methods=['GET'])
def tracking():
	user_id = request.args.get('uid')
	campaign_id = request.args.get('cid')
	email_id = request.args.get('eid')
	link_id= request.args.get('lid')
	if link_id != None:
		trackemail = Trackemail.query.filter_by(user_id=user_id, campaign_id=campaign_id, email_id=email_id).first()
		if trackemail == None:
			track1 = Trackemail(user_id,campaign_id,email_id)
			db.session.add(track1)
			db.session.commit()
			trackemail = Trackemail.query.filter_by(user_id=user_id, campaign_id=campaign_id, email_id=email_id).first()
		tracklink1 = Tracklink(trackemail.trackemail_id,link_id)
		db.session.add(tracklink1)
		db.session.commit()
		product = Products.query.filter_by(product_id=link_id).first()
		url = product.url
		return redirect(url)		
	else:
		track1 = Trackemail(user_id,campaign_id,email_id)
		db.session.add(track1)
		db.session.commit()
		return redirect(url_for('track.static', filename='img/pixel.png'))


@track.route("/send", methods=['POST'])
def send():
	if 'email' not in session:
		return redirect(url_for('login.signin'))
	user = Users.query.filter_by(email=session['email']).first()
	campaign= Campaign.query.filter_by(campaign_id=request.form['cid']).first()
	emails= Email.query.filter_by(list_id=campaign.list_id).all()
	product = Products.query.filter_by(campaign_id=campaign.campaign_id).first()
	sendtemplate = Templates.query.filter_by(campaign_id=campaign.campaign_id).first()
	templatehtml = Template(sendtemplate.html)
	templatetxt = Template(sendtemplate.txt)
	with mail.connect() as conn:
	    for email in emails:
	    	msg = Message(sendtemplate.subject,sender=(sendtemplate.sender_name, sendtemplate.sender_email))
	    	msg.recipients = [email.email]
	    	url_pix = request.url_root + 'track/track?'+ 'uid=' + str(user.user_id) + '&cid=' + str(campaign.campaign_id) + '&eid=' + str(email.email_id)
	    	url = url_pix + '&lid=' + str(product.product_id)
	    	msg.body = templatetxt.render(email = email, url = url, url_pix = url_pix)
	    	msg.html = templatehtml.render(email = email, url = url, url_pix = url_pix)
	    	conn.send(msg)
	return 'Ok'
