import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users' #how to declare a table name on SQLAlchemy

    id = db.Column(db.Integer, primary_key =  True) #primary key just means it's unique and makes it easier to search.
    username = db.Column(db.String(80))
    password = db.Column(db.String(80)) #80 is the character limit.

    def __init__(self, username, password):
        #self.id = _id we got rid of this because it's already auto incrementing. We don't need it as another object of the Userclass.
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first() #SELECT * FROM items WHERE name = name LIMIT 1 which returns the first row only

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first() #SELECT * FROM items WHERE name = name LIMIT 1 which returns the first row only

#this is an API that exposes two endpoints. The find_by_username and find_by_id.
#It's a way for our program to interact with our user.
