from peewee import CharField, IntegerField, Model, SqliteDatabase, ForeignKeyField

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

class Customer(BaseModel):
    name = CharField()
    age = IntegerField()

class Cart(BaseModel):
    customer = ForeignKeyField(Customer, backref='carts')

class CartItem(BaseModel):
    cart = ForeignKeyField(Cart, backref='items')
    item = ForeignKeyField(Item, backref='carts')

