from flask import render_template, request, flash, session, url_for, redirect, Blueprint
from flask_mail import Mail, Message
from app.login.forms import ContactForm, SignupForm, SigninForm
from app.models import *
from app.track.views import mail

login = Blueprint('login',__name__, static_folder='static', template_folder='templates', url_prefix='/home')


@login.route('/')
def home():
  return render_template('home.html')

@login.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()

  if 'email' in session:
    return redirect(url_for('login.profile')) 
  
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = Users(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      
      session['email'] = newuser.email
      return redirect(url_for('login.profile'))
  
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@login.route('/profile')
def profile():

  if 'email' not in session:
    return redirect(url_for('login.signin'))

  user = Users.query.filter_by(email = session['email']).first()
  campaigns= Campaign.query.filter(Campaign.user_id==user.user_id).count()
  template = Templates.query.filter_by(user_id=user.user_id).count()
  lists = Lists.query.filter_by(user_id=user.user_id).count()
  tracks = Trackemail.query.filter_by(user_id=user.user_id).count()
  data = { 'campaigns' : campaigns, 'template' : template , 'lists' : lists , 'track' : tracks}
  return render_template('profile.html', data=data)

@login.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()

  if 'email' in session:
    return redirect(url_for('login.profile')) 
      
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('login.profile'))
                
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@login.route('/signout')
def signout():

  if 'email' not in session:
    return redirect(url_for('login.signin'))
    
  session.pop('email', None)
  return redirect(url_for('login.home'))


# @login.route('/contact', methods=['GET', 'POST'])
# def contact():
#   form = ContactForm()

#   if request.method == 'POST':
#     if form.validate() == False:
#       flash('All fields are required.')
#       return render_template('contact.html', form=form)
#     else:
#       msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@example.com'])
#       msg.body = """
#       From: %s <%s>
#       %s
#       """ % (form.name.data, form.email.data, form.message.data)
#       mail.send(msg)

#       return render_template('contact.html', success=True)

#   elif request.method == 'GET':
#     return render_template('contact.html', form=form)