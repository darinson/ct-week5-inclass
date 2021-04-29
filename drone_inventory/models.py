from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

#Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

#Import for Secrets Module (Provided by Python)
import secrets

#Imports for Login Manager and the UserMixin
from flask_login import LoginManager, UserMixin

#Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow #A class, denoted by uppercase M

#Instantiate sqlalchemy 
db = SQLAlchemy()

#Instantiate Login Manager
login_manager = LoginManager()

#Instantiate Marshmallow
ma = Marshmallow() # also need to initialize it in the init


@login_manager.user_loader
#attribute user_loader for object login_manager. 
#decorator allows us to access the function within a function. 
#we get user_id from user_loader using the decorator above it
def load_user(user_id): #user_id will come from user_loader
    #get the user that is currently logged in using their user id
    #aka call back function
    return User.query.get(user_id) #query.get syntax is similar to SQL get.

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '') #No limit on string characters, because we are going to encrypt it and want it to be as large as it needs to be
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    drone = db.relationship('Drone', backref = 'owner', lazy = True) #Drone referring to the drone class below, only loads it when we need it (lazy)
    #this can only be done bby one user at a time

    def __init__(self,email,first_name = '', last_name = '', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'User {self.email} has been created and added to database!'

class Drone(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.String(150))
    cam_quality = db.Column(db.String(150), nullable = True)
    flight_time = db.Column(db.String(100), nullable = True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    cost_of_prod = db.Column(db.String(150))
    series = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    
    def __init__(self,name,description,price,cam_quality,flight_time,max_speed,dimensions,weight,cost_of_prod,series,user_token,id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.cam_quality = cam_quality
        self.flight_time = flight_time
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_prod = cost_of_prod
        self.series = series
        self.user_token = user_token
        
    def __repr__(self):
        return f'The following Drone has been added: {self.name}'

    def set_id(self):
        return secrets.token_urlsafe()


#Creation of API Schema via the marshmallow package
class DroneSchema(ma.Schema):
    class Meta:
        fields = ['id','name','description','price','cam_quality','flight_time', 'max_speed', 'dimensions', 'weight', 'cost_of_prod', 'series']


drone_schema = DroneSchema() #dict
drones_schema = DroneSchema(many = True) #returns list of dicts