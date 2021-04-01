from datetime import datetime
from decimal import Decimal
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json
from werkzeug.middleware.proxy_fix import ProxyFix
from wtforms import Form, StringField, IntegerField, validators

# CONFIG
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


def db_uri():
    params = {
        'host' : 'postgres',
        'port' : 5432,
        'database' : 'usersnack',
        'user' : 'adrian',
        'password' : 'db-pass',
    }
    return f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"


app.config['SQLALCHEMY_DATABASE_URI'] = db_uri()
db = SQLAlchemy(app)

AWS_S3_URL = 'https://usersnack.s3.us-east-2.amazonaws.com/'


# MODELS
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


# FORMS
class SubmitForm(Form):
    name = StringField('Name')
    address = StringField('Address', [validators.Length(min=6, max=50)])
    pizza = IntegerField('Pizza')


# VIEWS
@app.route('/')
def home():
    #TODO: ReactJS front
    return 'home'


@app.route('/orders')
def orders():
    response = Order.get_all()
    return json.dumps(response)


@app.route('/pizzas')
def pizza_list():
    data = Pizza.get_all()
    # print(data, flush=True)
    return json.dumps(data)


@app.route('/pizzas/<int:pizza_id>')
def pizza_detail(pizza_id):
    response = {}
    response['Pizza'] = Pizza.get_one(pizza_id)
    response['Extras'] = Extra.get_all()
    return json.dumps(response)


@app.route('/pizzas/submit', methods=['POST'])
def pizza_submit():
    form = SubmitForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['name']
        address = request.form['address']

        pizza = Pizza.get_one(request.form['pizza'])
        description = f'Pizza: {pizza["name"]} | Price {pizza["price"]}'
        total_amount = Decimal(pizza['price'])

        for extra_id in request.form['extra'].split(','):
            extra = Extra.get_one(extra_id)
            description += f', Extra: {extra["name"]} | Price {extra["price"]}'
            total_amount += Decimal(extra['price'])

        order = Order(name, address, total_amount, description)
        db.session.add(order)
        db.session.commit()

        return json.dumps(str(total_amount))
    else:
        #TODO: Send http error
        return 'HTTP METHOD OR FORM INCORRECT'


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
