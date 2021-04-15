#This is the authentication blueprint

from flask import Blueprint, render_template, request, flash, redirect, url_for
from drone_inventory.forms import UserLoginForm
from drone_inventory.models import User, db, check_password_hash

#Imports for flash login
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth',__name__,template_folder='auth_templates')

@auth.route('/signup',methods=['GET','POST'])
def signup():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)

            db.session.add(user) #insert statement!!!
            db.session.commit()
            
            flash(f'You have successfully created a user account{email}', 'user-created') #flash from the Flask package

            return redirect(url_for('site.home')) #from Flask package
    except:
        raise Exception('Invalid Form Data: Please Check Your Form Inputs')
    
    return render_template('signup.html', form = form) #What other contexts are avaiable? (input argument for render_template function)

@auth.route('/signin', methods=['GET','POST'])
def signin():
    form = UserLoginForm() #Instantiating UserLoginForm

    try:
        if request.method == 'POST' and form.validate_on_submit():
            #'POST' from form.html
            #form.validate_on_submit from forms.py(validator)
            email = form.email.data
            password = form.password.data
            print(email,password)

            logged_user = User.query.filter(User.email == email).first() 
            #flask shell in virtual_env in cmd
            #logged_user is instantiating a User class (similar to GRABBING A ROW FROM THE SQL TABLE) using the filter email = email.
            #similar to where clause in sql, Where email in table = email that was entered into this function
            if logged_user and check_password_hash(logged_user.password, password):
                #if we find email and the same password
                login_user(logged_user) #from flask login (the login_user)
                flash('You were successfully logged in: via email/password', 'auth-sucess') #category of auth-success, which we will use in html
                
                return redirect(url_for('site.home'))
            else:
                flash('Your email/password is incorrect', 'auth-failed')

                return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: PLease Check Your Form')

    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required #need to import
def logout():
    logout_user() #need to import
    return redirect(url_for('site.home'))