from peewee import *

db = SqliteDatabase('apartments.db')

class BaseModel(Model):
    class Meta:
        database = db
        only_save_dirty = True

class Apartment_Type(BaseModel):
    entrance = IntegerField()
    name = CharField()
    floors = IntegerField()
    apt_on_floor = IntegerField()
    
class Apartment(BaseModel):
    apt_id = IntegerField()
    region = CharField(120)
    city = CharField(120)
    type = ForeignKeyField(Apartment_Type, backref='apartments')
    chat_url = CharField()
    
class User(BaseModel):
    user_id = IntegerField(unique=True)
    name = CharField(120)
    apt = ForeignKeyField(Apartment, backref='users')

if __name__=='__main__':
    all_tables = BaseModel.__subclasses__()
    db.drop_tables(all_tables)
    db.create_tables(all_tables)

