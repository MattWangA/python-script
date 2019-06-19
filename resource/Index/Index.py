from flask_restful import Resource
from resource.Index import simple_page

@simple_page.route('/')
def index():
    return "Hello"