from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate,identity

app = Flask(__name__)
app.secret_key = 'Mariano'
api = Api(app)

jwt = JWT (app, authenticate, identity) #/auth

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank, fill it"
                        )
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items),None)
        #Is the function doesnt get an item it returns a None

        return {"item": item}, 200 if item else 404

    def post(self,name):
        if next(filter(lambda x: x['name'] == name, items),None):
            return {'message': "The item '{}' already exists.".format(name)}, 400
        #Si colocamos entre parentesis force=True ignora la cabecera, es peligroso
        #pero si colocamos silent = True, me devuelve un None si la cabecera es incorrecta
        #asi obtenemos el Json payload
        #Si el request no tiene un dato o un json format, va a dar error
        #En el postman tengo que tener bien el content-Type y el tipo de aplicacion
        data = Item.parser.parse_args()
        # request_data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 #El 201 es el codigo http que indica creado
    #el 202 indica aceptado pero puede demorar mas en crear

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            # item = {'name': name,'price': data['price']}
            item.update(data)
        return item


class Itemlist(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item,'/item/<string:name>')
api.add_resource(Itemlist, '/items')


app.run(port=8000, debug=True)