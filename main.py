from flask import Flask,Blueprint
from flask_restful import Resource, Api
from resource.Index.Index import simple_page
from resource.excel.excel import excel


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


app = Flask(__name__)
api = Api(app)
app.register_blueprint(simple_page,url_prefix='/Index')
app.register_blueprint(excel,url_prefix='/New_joiner')
app.after_request(after_request)



if __name__ == '__main__':
    app.run(host='10.20.11.85',debug = True)
      # app.run(debug=True)