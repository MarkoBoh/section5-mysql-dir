from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.item import Item, ItemList
from resources.user import  UserRegister, Users
from security import authenticate, identity
  
app = Flask(__name__)
app.secret_key = 'MarkoGeslo'
api = Api(app)

jwt = JWT(app,authenticate,identity)   # s tem dobimo nov endpoint /auth

api.add_resource(Item,'/item/<string:name>') # http://127.0.0.1:5000/item/omara
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Users,'/users')

if __name__ == '__main__': # ce smo v glavnem modulu, pozeni, sicer pa ne, ker smo v import knjiznici
                            # python modulu, ki ga pozenemo, doloci flag __main__
    app.run(host="0.0.0.0",debug=True) # p5000 je sicer default, lahko ni izpustili

 