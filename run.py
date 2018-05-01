from app import app
from db import db

db.init_app(app)

@app.before_first_request #so you don't have to run the create tables script anymore.
def create_tables():
	db.create_all()
