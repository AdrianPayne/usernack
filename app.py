from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/')
def home():
    return 'This is the home'


@app.route('/pizzas')
def pizza_list():
    return {
        '_': 'pizza_list',
        'content': {
            'pizza_1': 'Margarita',
            'pizza_2': 'Diabola',
        },
    }


@app.route('/pizzas/<int:pizza_id>')
def pizza_detail(pizza_id, methods=['GET', 'POST']):
    if request.method == 'POST':
        response = f'This is a POST for {pizza_id}'
    else:
        response = f'This is a GET for {pizza_id}'

    return response


if __name__ == '__main__':
    app.run()
