from flask import Flask
from flask_restful import Api #reqparse is actually not a part of flask restful.
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
#a resource  is just a thing our API returns and creates. It's a vague term.
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #The SQLAlchemy is going to live at the root folder of our project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #i have no idea what this does.
app.secret_key = 'ryhan'
api = Api(app) #Allow us to easily add resources to it.



jwt = JWT(app, authenticate, identity) #creates a new endpoint /auth. we send a username and password and the jwt gets the username and password and sends it to the authenticate function

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	from db import db # if we import db and the models at the top. It'll create a circular import which wouldn't work.
	db.init_app(app)
	app.run(port=5000, debug = True) #if we import app, we create the flask app. If we import, then we would always run when we don't want it to.
