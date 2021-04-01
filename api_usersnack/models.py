from datetime import datetime
from api_usersnack.app import db, AWS_S3_URL


class Extra (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Numeric(5, 2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f'<name {self.name}>'

    @staticmethod
    def get_all():
        all_objects = Extra.query.all()
        response = []
        for item in all_objects:
            item_data = {
                'id': item.id,
                'name': item.name,
                'price': str(item.price)
            }
            response.append(item_data)
        return response

    @staticmethod
    def get_one(id):
        item = Extra.query.get(id)
        item_data = {
            'id': item.id,
            'name': item.name,
            'price': str(item.price),
        }
        return item_data


class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Numeric(5, 2))
    ingredients = db.Column(db.String())
    img = db.Column(db.String())

    @staticmethod
    def get_all():
        all_objects = Pizza.query.all()
        response = []
        for item in all_objects:
            item_data = {
                'id': item.id,
                'name': item.name,
                'price': str(item.price),
                'ingredients': item.ingredients,
                'img': AWS_S3_URL + item.img
            }
            response.append(item_data)
        return response

    @staticmethod
    def get_one(id):
        item = Pizza.query.get(id)
        item_data = {
            'id': item.id,
            'name': item.name,
            'price': str(item.price),
            'ingredients': item.ingredients,
            'img': AWS_S3_URL + item.img
        }
        return item_data

    def __init__(self, name, price, ingredients, img):
        self.name = name
        self.price = price
        self.ingredients = ingredients
        self.img = img

    def __repr__(self):
        return f'<name {self.name}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    name = db.Column(db.String())
    address = db.Column(db.String())
    total_amount = db.Column(db.Numeric(7, 2))
    description = db.Column(db.String())

    def __init__(self, name, address, total_amount, description):
        self.name = name
        self.created = datetime.now()
        self.address = address
        self.total_amount = total_amount
        self.description = description

    def __repr__(self):
        return f'<id {self.id}>'

    @staticmethod
    def get_all():
        all_objects = Order.query.all()
        response = []
        for item in all_objects:
            item_data = {
                'id': item.id,
                'name': item.name,
                'created': item.created.strftime("%d/%m/%Y %H:%M:%S"),
                'address': item.address,
                'total_amount': str(item.total_amount),
                'description': item.description
            }
            response.append(item_data)
        return response