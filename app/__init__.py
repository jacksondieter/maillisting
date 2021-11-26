from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from app import models
from app.models import db
from app.core.views import core
from app.login.views import login
from app.track.views import track,mail

app = Flask(__name__)

app.register_blueprint(core, url_prefix='/dash')
app.register_blueprint(login, url_prefix='/home')
app.register_blueprint(track, url_prefix='/track')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/maillist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

app.secret_key = 'development key'

app.config.update( MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 587,
	MAIL_USE_TLS = True,
	MAIL_USERNAME = 'pypyguru@gmail.com',
	MAIL_PASSWORD = 'k8k7k6k5',
	MAIL_DEFAULT_SENDER = ('Pypi', 'pypyguru@gmail.com'))

mail.init_app(app)

app.debug = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)