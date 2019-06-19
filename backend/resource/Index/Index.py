from flask_restful import Resource
from backend.resource.Index import simple_page

@simple_page.route('/')
def index():
    return "Hello"