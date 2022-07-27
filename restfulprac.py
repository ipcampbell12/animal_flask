from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

# import other files for this app
from security import authenticate, identity
from user import UserRegister
from item import Animal,AnimalList

app = Flask(__name__)
app.secret_key = "Ian"
api = Api(app)

jwt = JWT(app, authenticate, identity)

# define animal resource


# add resource to api
api.add_resource(AnimalList, '/animals')
api.add_resource(UserRegister,'/register')
api.add_resource(Animal, '/animal/<string:type>')


app.run(port=5005, debug=True)
