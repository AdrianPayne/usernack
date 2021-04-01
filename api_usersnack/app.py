import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

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


from decimal import Decimal
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
    from models import Pizza, Extra, Order
    from forms import SubmitForm

    app.run('0.0.0.0', debug=True)
