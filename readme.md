# USERSNACK
Usersnack is a Flask and Postgresql API backend project. Simulate an API of a Pizza restaurant to show the offer and send orders.

In live on [AWS](http://13.59.120.109:5000/pizzas)!

## API Documentation

|        Resource        | Method |                              Description                              |                                            Form                                           |
|:----------------------:|:------:|:---------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------:|
| /pizzas                | GET    | Return a list of all available pizzas                                 |                                                                                           |
| /pizzas/<int:pizza_id> | GET    | Return details of the selected pizza and extra ingredients to add     |                                                                                           |
| /pizzas/submit         | POST   | Generate an order stored in DB. Return the total amount of the order. | name: String, address: String(min 6, max 50), pizza: Integer (pizza_id),extras: IntegerList |
| /orders                | GET    | Return a list of all stored orders                                    |                                                                                           |

## PREREQUISITES
1. Install Docker (https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
2. Install Docker-Compose (https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04)
3. Git clone the project

## RUN
docker-compose-build && docker-compose up

#### Start ORM and migration system
1. Run docker-compose
2. docker exec -it usernack_api-usersnack_1 bash
3. python3 manage.py db init
4. python3 manage.py db migrate
5. python3 manage.py db upgrade

#### Initial data
1. docker exec -it usernack_api-usersnack_1 bash
2. python3 command_initial_data.py

#### Reset Database
1. docker-compose down --volumes
2. Remove migrations folder
3. Create migration files again after run docker-compose