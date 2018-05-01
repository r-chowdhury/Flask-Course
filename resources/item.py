from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#resources are used for endpoints.

class Item(Resource): #inherits from the class resource. It's a copy of the resource class and we can also change things.
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required = True, help = 'This field cannot be left blank!') #we only defined price. if we put anything else on the json payload, they won't get defined.
    parser.add_argument('store_id', type=int, required = True, help = 'Every item needs a store id.') #we only defined price. if we put anything else on the json payload, they won't get defined.

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found'}, 404

    def post(self, name): #needs to have the same set of parameters. That name is going to come from the name here. Even though the request has a json payload, we are going to receive it through the URL.
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args() #we look for errors first, if they happen, we stop and break. Then we start parsing.

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500 #server had a problem.

        return item.json(), 201

    def delete(self, name): #very bad python event that we need to be conscientious of.
        item = ItemModel    .find_by_name(name)
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
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} #returns all the items in the database
