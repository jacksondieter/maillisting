from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, PasswordField, FileField, validators, ValidationError,SelectField,HiddenField
import re
from app.models import *

class CampaignForm(Form):
  campaign_id = HiddenField()
  product_id = HiddenField()
  method = HiddenField()
  name = TextField("Name",  [validators.Required("Please enter your Campaign name.")])
  product = TextField("Product",  [validators.Required("Please enter your Product name.")])
  url = TextField("URL",  [validators.Required("Please enter a url."), validators.URL("Please enter a url.")])
  list_templates = SelectField('Templates',coerce=int)
  list_lists = SelectField('Lists',coerce=int)
  submit = SubmitField("Campaign")


class TemplateForm(Form):
  template_id = HiddenField()
  method = HiddenField()
  name = TextField("Name",  [validators.Required("Please enter your Campaign name.")])
  subject = TextField("Subject",  [validators.Required("Please enter your Campaign name.")])
  sender_name = TextField("Sender_name",  [validators.Required("Please enter your sender name.")])
  sender_email = TextField("Sender_email",  [validators.Required("Please enter your sender email address."), validators.Email("Please enter your sender email address.")])
  htmlfile = FileField("Html")
  txtfile = TextAreaField("Txt")
  submit = SubmitField("Template")

class ListForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your Campaign name.")])
  maillistfile = FileField("Maillist")
  submit = SubmitField("Create List")

  
class myForm(Form):
  sender_name = TextField("Sender_name",  [validators.Required("Please enter your sender name.")])
  sender_email = TextField("Sender_email",  [validators.Required("Please enter your sender email address."), validators.Email("Please enter your sender email address.")])
  htmlfile = FileField("Html")
  txtfile = TextAreaField("Txt",  [validators.Required("Please enter a message.")])
  list_templates = SelectField('Templates')
  list_lists = SelectField('Lists')