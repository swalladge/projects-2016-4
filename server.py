from tornado.ncss import Server


def login_check_decorator(fn):
    def inner(response,*args, **kwargs):
        username1 =  response.get_secure_cookie('username')
        if username1 is None:
            return response.redirect('/account/login')
        return fn(response, *args, **kwargs)
    return inner

def index_handler(response):
    response.write('Hello Team 4: Placebook!')

def signup_handler(response):
    response.write('Sign Up')

def login_handler(response):
    file = open('test_login_form.html')
    response.write(file.read())

def search_handler(response):
    response.write("Search")

def location_handler(response, id):
    response.write("Location {}".format(id))

def create_handler(response):
    response.write("Create Location")

def user_handler(response, username):
    response.write("Profile {}".format(username))

@login_check_decorator
def profile_handler(response):
    username1 = response.get_secure_cookie('username')
    response.write("username: {}".format(str(username1)))

def login_authentication(response):
    username = response.get_field('username')
    password = response.get_field('password')
    if username == 'james' and password == 'curran':
        response.write('Logged in successfully')
        response.set_secure_cookie('username', username)
    else:
        response.write('Incorrect username or password')

if __name__ == '__main__':
    server = Server()
    server.register('/', index_handler)
    server.register("/account/signup",signup_handler)
    server.register("/account/login", login_handler, post=login_authentication)
    server.register("/location/search", search_handler)
    server.register(r"/location/(\d+)", location_handler)
    server.register("/location/create", create_handler)
    server.register("/account/profile/([a-z0-9A-Z._]+)", user_handler)
    server.register("/account/profile", profile_handler)
    server.run()
