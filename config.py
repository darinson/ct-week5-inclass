import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Giving access to the project in ANY OS we find ourselves in
# Allow outside files/folders to have the ability to add to the project from 
# the base directory
# We don't plan on changing the name or the location of the file, so we are using absolute path

class Config(): #this is a class by convention
    """
    We will set Config variables for the Flask App here.
    Using Environment variables where available, otherwise
    we will create the config variables(s) if not already done.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'You will never guess...' #So we can use form
    #SQLALCEHMY is the object relational mapper that will allow us to use python and sql
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db') #if the latter shows up, we know something is wrong.
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Turn off update messages from the database

