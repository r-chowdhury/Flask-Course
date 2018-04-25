from db import db

class ItemModel(db.Model):
	__tablename__ = 'items'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision = 2)) #2 = number of decimal places. Currency usually doesn't go past 2 decimal places.

	store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
	store = db.relationship('StoreModel') #equivalent to "join" on sql.
	#store id is the primary key
	#store id in the item is the foreign key. it has the values identical to another value in another table.s

	def __init__(self, name, price, store_id):
		self.name = name
		self.price = price
		self.store_id = store_id

	def json(self):
		return {'name': self.name, 'price': self.price}

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
