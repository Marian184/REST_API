from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items),None)
        #Is the function doesnt get an item it returns a None

        return {'item': None}, 200 if item else 404

    def post(self,name):
        if next(filter(lambda x: x['name'] == name, items),None):
            return {'message': "The item '{}' already exists.".format(name)}, 400
        request_data = request.get_json()
        #Si colocamos entre parentesis force=True ignora la cabecera, es peligroso
        #pero si colocamos silent = True, me devuelve un None si la cabecera es incorrecta
        #asi obtenemos el Json payload
        #Si el request no tiene un dato o un json format, va a dar error
        #En el postman tengo que tener bien el content-Type y el tipo de aplicacion

        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return item, 201 #El 201 es el codigo http que indica creado
    #el 202 indica aceptado pero puede demorar mas en crear

class Itemlist(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item,'/item/<string:name>')
api.add_resource(Itemlist, '/items')


app.run(port=8000, debug=True)