from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'dev-token'
api = Api(app)

# /auth is created which will provide token
jwt = JWT(app, authenticate, identity)

# In memory database
items = [

]

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field can't be left blank"
                        )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item": item}, 200 if item  else 404

    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': f'An item with name {name} already exists'}, 400
        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        return item, 201

    @jwt_required()
    def put(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        data = Item.parser.parse_args()
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
            return item, 201
        else:
            item.update(data)
            return item, 200

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': f'Item deleted {name}'}

class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}

# Route registration using flask_restful library.
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)


