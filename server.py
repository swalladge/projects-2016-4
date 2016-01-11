from template.render import render
from tornado.ncss import Server
from db.db import User, Location
import re

def get_login(response):
    return response.get_secure_cookie('username')

def login_check_decorator(fn):
    def inner(response, *args, **kwargs):
        username1 = response.get_secure_cookie('username')
        if username1 is None:
            return response.redirect('/account/login')
        return fn(response, *args, **kwargs)
    return inner

def render_page(filename, response, context):
    context['logged_in'] = get_login(response)
    if context['logged_in']:
        user = User.find(context['logged_in'])
        context['user'] = user
    html = render(filename, context )
    response.write(html)

def index_handler(response):
    render_page('index.html', response, {})

def signup_handler(response):
    logged_in = get_login(response)
    if logged_in is not None:
        response.redirect('/')
    else:
        render_page('register.html', response, {})

def login_handler(response):
    logged_in = get_login(response)
    if logged_in is not None:
        response.redirect("/account/profile")
    else:
        render_page('login.html', response, {})

def search_handler(response):
    logged_in = get_login(response)
    response.write("Search")

def location_handler(response, id):
    pass

@login_check_decorator
def create_handler(response):
    logged_in = get_login(response)
    response.write("Create Location")

@login_check_decorator
def user_handler(response, username):
    logged_in = get_login(response)
    response.write("Profile {}".format(username))

@login_check_decorator
def profile_handler(response):
    logged_in = get_login(response)
    response.write("username: {}".format(logged_in))

def login_authentication(response):
    username = response.get_field('username')
    password = response.get_field('password')
    user = User.find(username)
    if user and username == user.username and password == user.password:
        response.set_secure_cookie('username', username)
        response.redirect("/")
    else:
        response.write('Incorrect username or password')

def signup_authentication(response):
    username = response.get_field('username')
    password = response.get_field('password')
    c_password = response.get_field('confirm_password')
    fname = response.get_field('fname')
    lname = response.get_field('lname')
    email = response.get_field('email')
    user = User.find(username)
    context = {'error': None }
    if user:
        context["error"] = "Username taken"
    elif not username or not password or not email:
        context["error"] = "Username, password and email are required"
    elif password != c_password:
        context["error"] = "Passwords do not match"
    elif not re.match(r"^[0-9a-zA-Z_\.]+$", username):
        context["error"] = "Invalid username, please use only letters, numbers, underscores and periods"
    else:
        User.create(username, password, None, email, fname, lname)
        response.set_secure_cookie('username', username)
        response.redirect("/")
        return None
    render_page('register.html', response, context)

def logout_handler(response):
    response.clear_cookie("username")
    response.redirect("/")

@login_check_decorator
def location_creator(response):
    pass

if __name__ == '__main__':
    server = Server()
    server.register('/', index_handler)
    server.register("/account/signup",signup_handler, post=signup_authentication)
    server.register("/account/login", login_handler, post=login_authentication)
    server.register("/location/search", search_handler)
    server.register(r"/location/(\d+)", location_handler)
    server.register("/location/create", create_handler, post=location_creator)
    server.register("/account/profile/([a-z0-9A-Z._]+)", user_handler)
    server.register("/account/profile", profile_handler)
    server.register("/account/logout", logout_handler)
    server.run()
