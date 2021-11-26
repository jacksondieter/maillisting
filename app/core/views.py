from flask import Flask, request, redirect, url_for, render_template, Blueprint , flash, session
from flask_sqlalchemy import SQLAlchemy
from app.core.forms import CampaignForm,TemplateForm,ListForm,myForm
import re
from app.models import *

core = Blueprint('core',__name__, static_folder='static', template_folder='templates', url_prefix='/dash') 

@core.route('/campaign', methods=['GET','POST','PUT','DELETE'])
def campaign():
	form = CampaignForm()
	form.list_templates.choices = [(g.template_id, g.name) for g in Templates.query.order_by('name')]
	form.list_lists.choices = [(g.list_id, g.name) for g in Lists.query.order_by('name')]
	if 'email' not in session:
		return redirect(url_for('login.signin'))
	user = Users.query.filter_by(email=session['email']).first()
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields to create a campaign are required.')
		elif form.method.data == 'PUT':
			editcampaign = Campaign.query.filter_by(campaign_id=form.campaign_id.data).first()
			editcampaign.name = form.name.data
			editcampaign.list_id = form.list_lists.data
			db.session.commit()
			editproduct = Products.query.filter_by(product_id=form.product_id.data).first()
			editproduct.name = form.product.data
			editproduct.url = form.url.data
			db.session.commit()
			edittemplate = Templates.query.filter_by(template_id=form.list_templates.data).first()
			edittemplate.campaign_id=editcampaign.campaign_id
			db.session.commit()			
		else:
			newcampaign = Campaign(form.name.data, user.user_id,form.list_lists.data)
			db.session.add(newcampaign)
			db.session.commit()
			readcampaign = Campaign.query.filter_by(name=form.name.data).first()
			newproduct = Products(form.product.data, form.url.data, readcampaign.campaign_id)
			db.session.add(newproduct)
			db.session.commit()
			readtemplate = Templates.query.filter_by(template_id=form.list_templates.data).first()
			readtemplate.campaign_id=readcampaign.campaign_id
			db.session.commit()

	if request.method == 'DELETE':
		edittemplate = Templates.query.filter_by(campaign_id=request.form['cid']).first()
		print(edittemplate)
		if edittemplate != None:
			edittemplate.campaign_id = None
			db.session.commit()
		editproduct = Products.query.filter_by(campaign_id=request.form['pid']).first()
		db.session.delete(editproduct)
		db.session.commit()
		trackemail = Trackemail.query.filter_by(campaign_id=campaign.campaign_id).all()
		tracklink = Tracklink.query.join(Trackemail).filter(Trackemail.campaign_id==campaign.campaign_id).filter(Tracklink.trackemail_id == Trackemail.trackemail_id).all()
		db.session.delete(trackemail)
		db.session.commit()
		db.session.delete(tracklink)
		db.session.commit()
		editcampaign = Campaign.query.filter_by(campaign_id=request.form['cid']).first()
		db.session.delete(editcampaign)
		db.session.commit()


	campaigns= Campaign.query.filter(Campaign.user_id==user.user_id).all()
	campaigndata = []
	for campaign in campaigns:
		product = Products.query.filter_by(campaign_id=campaign.campaign_id).first()
		emails= Email.query.filter_by(list_id=campaign.list_id).count()
		trackemail = Trackemail.query.filter_by(campaign_id=campaign.campaign_id).count()
		tracklink = Tracklink.query.join(Trackemail).filter(Trackemail.campaign_id==campaign.campaign_id).filter(Tracklink.trackemail_id == Trackemail.trackemail_id).count()
		campaigndata.append({'campaign':campaign , 'product' : product , 'emails' : emails , 'trackemail':trackemail ,'tracklink':tracklink})
	return render_template('campaign.html', campaign=campaigndata, form=form)

@core.route('/templates', methods=['GET','POST','PUT','DELETE'])
def templates():
	form = TemplateForm()
	user = Users.query.filter_by(email=session['email']).first()
	if 'email' not in session:
		return redirect(url_for('login.signin'))

	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields to create a template are required.')
		
		elif form.method.data != 'PUT':
			file_data = request.files[form.htmlfile.name]
			if file_data and allowed_file(file_data.filename,'html') and form.validate() == True:		
				filehtml=file_data.read().decode('utf-8')
				padrao1=re.compile('<a.*href="\S*"')
				padrao2=re.compile('<body>')
				html_mod=re.subn(padrao1, '<a href="{{url}}"', filehtml)
				html_mod=re.subn(padrao2, '<body><img src="{{ url_pix }}" alt="." height="1" width="1">', html_mod[0])
				if html_mod[1]==0:
					padrao3=re.compile(r'^')
					html_mod=re.sub(padrao3, '^<img src="{{ url_pix }}" alt="." height="1" width="1">', html_mod[0])
				newtemplate = Templates(form.name.data,form.subject.data, form.sender_name.data, form.sender_email.data, html_mod[0], form.txtfile.data, user.user_id)
				db.session.add(newtemplate)
				db.session.commit()
		
		
		else:
			edittemplate = Templates.query.filter_by(template_id=form.template_id.data).first()
			edittemplate.name = form.name.data
			edittemplate.subject = form.subject.data
			edittemplate.sender_name = form.sender_name.data
			edittemplate.sender_email = form.sender_email.data
			edittemplate.txt = form.txtfile.data
			db.session.commit()
		

	template = Templates.query.filter_by(user_id=user.user_id).all()
	print(template)
	templatedata = []
	for item in template:
		name = item.name
		campaign = Campaign.query.filter_by(campaign_id=item.campaign_id).first()
		if campaign==None:
			campaign_name="campaign not associated"
		else:
			campaign_name = campaign.name
		templatedata.append({'name':name , 'template' : item , 'campaign_name' : campaign_name})
	return render_template('templates.html',templates=templatedata, form=form)	

def allowed_file(filename,types):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] == types    

@core.route('/lists', methods=['GET','POST','DELETE'])
def lists():
	form = ListForm()
	user = Users.query.filter_by(email=session['email']).first()
	if 'email' not in session:
		return redirect(url_for('login.signin'))
	if request.method=='POST':
		if form.validate() == True:			
			file_data = request.files[form.maillistfile.name]
			if file_data and allowed_file(file_data.filename,'csv'):
				lista=Lists(form.name.data,user.user_id)
				db.session.add(lista)
				db.session.commit()
				file=str(file_data.read())
				padrao=re.compile('\w*@\w*[.]\w*\w')
				lista_matches=re.findall(padrao, file)
				lists = Lists.query.filter_by(name=form.name.data).first()
				for email in lista_matches:					
					email=Email(str(email),lists.list_id)
					db.session.add(email)
					db.session.commit()
	if request.method == 'DELETE':
		lista = Lists.query.filter_by(list_id=request.form['lid']).first()
		emails = Email.query.filter_by(list_id=request.form['lid']).all()
		for email in emails:
			db.session.delete(email)
			db.session.commit()
		db.session.delete(lista)
		db.session.commit()
	lists = Lists.query.filter_by(user_id=user.user_id).all()
	listsdata = []
	for item in lists:
		emails= Email.query.filter_by(list_id=item.list_id).count()
		listsdata.append({'list':item , 'emails' : emails})
	return render_template('lists.html', lists=listsdata, form=form)

@core.route('/template_create', methods=['GET','POST'])
def template_create():
	form = myForm()
	if 'email' not in session:
		return redirect(url_for('login.signin'))
	if request.method == 'POST':
		print(form.list_templates.data)
		print(form.list_lists.data)

	form.list_templates.choices = [(g.template_id, g.name) for g in Templates.query.order_by('name')]
	form.list_lists.choices = [(g.list_id, g.name) for g in Lists.query.order_by('name')]
	return render_template('templates_create.html',form=form)