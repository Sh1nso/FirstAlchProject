import json
from main import User, Order, Offer, db
from datetime import datetime


def get_data_from_json(path):
    with open(path, encoding='utf-8') as file:
        data = json.load(file)
    return data


def add_users_to_db():
    for user_data in get_data_from_json('data/users.json'):
        user = User(first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    age=user_data['age'],
                    email=user_data['email'],
                    role=user_data['role'],
                    phone=user_data['phone'])
        db.session.add(user)
    db.session.commit()


def add_offers_to_db():
    for offers_data in get_data_from_json('data/offers.json'):
        offer = Offer(order_id=offers_data['order_id'],
                      executor_id=offers_data['executor_id'])
        db.session.add(offer)
    db.session.commit()


def add_orders_to_db():
    for orders_data in get_data_from_json('data/orders.json'):
        order = Order(name=orders_data['name'],
                      description=orders_data['description'],
                      start_date=datetime.strptime(orders_data['start_date'], '%m/%d/%Y'),
                      end_date=datetime.strptime(orders_data['end_date'], '%m/%d/%Y'),
                      address=orders_data['address'],
                      price=orders_data['price'],
                      customer_id=orders_data['customer_id'],
                      executor_id=orders_data['executor_id'])
        db.session.add(order)
    db.session.commit()


db.drop_all()
db.create_all()
add_users_to_db()
add_offers_to_db()
add_orders_to_db()
