from flask_restful import Resource, reqparse
from flask_jwt import  jwt_required
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field can't be left blank"
                        )
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))

        row = result.fetchone()
        connection.close()
        if row:
            return {"item": {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert(cls, item):
        # Db connection
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO  items VALUES (?, ?)"
        result = cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()
        # Connection closed

    @classmethod
    def update(cls, item):
        # Db connection
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE   items SET price=? WHERE name=?"
        result = cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()
        # Connection closed

    @classmethod
    def delete(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE  FROM  items WHERE name=?"
        result = cursor.execute(query, (name,))

        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'item not found' }, 400

    @jwt_required()
    def post(self, name):
        # if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #     return {'message': f'An item with name {name} already exists'}, 400
        item = self.find_by_name(name)
        if item:
            return {'message': f'An item with name {name} already exists'}, 400
        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }
        try:
            self.insert(item)
            return item, 201
        except:
            return {'message': 'An error occured while inserting'}, 500 # Internal server error

    @jwt_required()
    def put(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = self.find_by_name(name)
        data = Item.parser.parse_args()
        updated_item = {
            'name': name,
            'price': data['price']
        }
        if item is None:
            try:
                self.insert(updated_item)
                return updated_item, 201
            except:
                return {'message': 'An error occured while inserting'}, 500  # Internal server error
        else:
            try:
                self.update(updated_item)
                return updated_item, 200
            except:
                return {'message': 'An error occured while inserting'}, 500  # Internal server error

    @jwt_required()
    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        try:
            self.delete(name)
            return {'message': f'Item deleted {name}'}
        except:
            return {'message': 'An error occured while deleting item'}, 500  # Internal server error

class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = list()
        for row in result:
            items.append(row)
        connection.close()
        return {'items': items}
