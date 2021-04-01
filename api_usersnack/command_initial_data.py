import json
import yaml

from app import db, Pizza, Extra

if __name__ == '__main__':

    with open("initial_data/data/data.json") as file:
        data_raw = file.read()
        data = yaml.load(data_raw)

        for item in data['Pizza']:
            name = item['name']
            price = item['price']

            ingredients = ""
            for i in item['incredients'][0].keys():
                ingredients += f'{i}, '
            ingredients = ingredients[:-2]

            img = item['img']

            item_to_insert = Pizza(name, price, ingredients, img)
            db.session.add(item_to_insert)
            db.session.commit()

        for item in data['Extras']:
            name = item['name']
            price = item['price']

            item_to_insert = Extra(name, price)
            db.session.add(item_to_insert)
            db.session.commit()
