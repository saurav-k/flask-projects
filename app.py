from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]

# Get '/' Home Page
@app.route('/')
def home():
    return render_template('index.html')

# POST /store data: {name:}   => To add a store
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store  => To get all store
@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores' : stores})

# GET /store/<string:name> => To get store by name
@app.route('/store/<string:name>', methods=['GET'])
def get_store_by_name(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'Store not found'})


# POST /store/<string:name>/item data: {name, price}  => To add a item in store
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'Store not found'})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item', methods=['GET'])
def get_items_from_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store['items'])
    return jsonify({'message': 'Store not found'})


if __name__ == '__main__':
    app.run()



# Jsonify