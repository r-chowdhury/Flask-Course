from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy='dynamic') #tells python/sql where the relationship is.
    #lazy = dynamic mean it's not longer an object. It's a query. Until we call the json method, we are not looking into the table.
    #which means creating stores is more simple.
    #but every time we call the json method, it looks into the table.
    #trade off between speed of creating the store and calling the json method.
    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod #should still be a classmethod because it's returning an object as opposed to a dictionary.
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #SELECT * FROM items WHERE name = name LIMIT 1 which returns the first row only

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        #when we retrieve an object from the db that has a particular id, then we can change the object's name. That's an update so this is a post and put method.


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

#this is an internal representation of what an item does and looks like.
