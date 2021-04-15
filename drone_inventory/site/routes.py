from flask import Blueprint, render_template #blueprint class
from flask_login import login_required

#create variable, same as the folder name, which is what we are creating
#Blueprint is a collection of routes. 
#Everything under site is for front end.
site = Blueprint('site',__name__,template_folder='site_templates')
#__name__ inherit the same name as the overall project (drone_inventory)

"""
Blueprint Configuration
The first argument, "site" is the Blueprint's name,
which is used by Flask's routing system.

The second argument, "__name__" is the Blueprint's import name,
which FLask uses to locate the Blueprint resources. 

The last argument, "template_folder", is the Blueprint's HTML template folder,
which tells the Blueprint which HTML files to use for specific routes.
"""

@site.route('/') #this is gonna be our main page. the url with a foreslash and 
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')