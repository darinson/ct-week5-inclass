from flask import Flask
from config import Config #config our file, Config the class we created in the file

from .site.routes import site
from .authentication.routes import auth
from .api.routes import api

from flask_migrate import Migrate
from .models import db as root_db, login_manager, ma

from flask_cors import CORS #prevent malware from possible sources. 

from .helpers import JSONEncoder

app = Flask(__name__)

app.config.from_object(Config) #we want to configure the object Config

app.register_blueprint(site) #we created site blueprint under routes.py in site folder
app.register_blueprint(auth) #we created auth blueprint under routes.py in authentication folder
app.register_blueprint(api)

root_db.init_app(app) #connecting sql alchemy and flask together
migrate = Migrate(app, root_db)
#Migrate -- when we are trying to edit the structure of the model (Sql table)

login_manager.init_app(app) #attaches the login manager to the app
login_manager.login_view = 'auth.signin'#Specifies what page to load for *non authorized* user
#restrict person who is not logged into the sign in area

ma.init_app(app)

CORS(app) #cross origin resource sharing, O stands for domain. cant share resources between domains unless there is something to go between. 
#Turning it on for development purposes so we can share across domains. Normally off so nothing can be shared across domains.

app.json_encoder = JSONEncoder #don't need to instantiate, because super(Jsonencoder, self) is already gonna call on itself.

from drone_inventory import models