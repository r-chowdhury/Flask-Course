from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#resources are used for endpoints.

class Item(Resource): #inherits from the class resource. It's a copy of the resource class and we can also change things.
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
    required=True,
    help = 'This field cannot be left blank!')

    parser.add_argument('store_id',
    type=int, required=True,
    help = 'Every item needs a store id.')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args() #we look for errors first, if they happen, we stop and break. Then we start parsing.

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item.'}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item =  ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} #returns all the items in the database
