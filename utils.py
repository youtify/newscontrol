from google.appengine.api import users
from model import User

def get_current_user_model():
    return get_user_model_for(users.get_current_user())

def get_user_model_for(google_user=None):
    return User.all().filter('google_user =', google_user).get()