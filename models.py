from flask import Flask
from flask import render_template
from flask import request
from peewee import CharField, IntegerField, Model, SqliteDatabase

#create flask application
app = Flask(__name__)

#creata a peewee database
database = SqliteDatabase('my_app.db')

#create standard baseModel
class BaseModel(Model):
	class Meta:
		database = database

#Item Model with its name and quantity as fields
class Item(BaseModel):
    name = CharField()
    quantity = IntegerField()

#function to create tables
def create_tables():
	with database:
		database.create_tables([Item])

@app.before_request
def before_request():
    database.connect()

@app.after_request
def after_request(response):
    database.close()
    return response

@app.route('/')
def index():
#Return index page of the web app
    return render_template('index.html')

@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'POST' and request.form['add']:
    	with database.atomic():
    		item = Item.create(
    			name=request.form['_'],
    			quantity=request.form[0])
    return render_template('items.html')		


if __name__ == '__main__':
    create_tables()
    app.run()
