from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils import get_user, get_order, get_offer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    age = db.Column(db.Integer)
    email = db.Column(db.Text)
    role = db.Column(db.Text)
    phone = db.Column(db.Text)

    orders = db.relationship('Order')
    offers = db.relationship('Offer')


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    orders = db.relationship('Order')


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    address = db.Column(db.Text)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('order.id'))


@app.route('/users')
def show_all_users():
    list_of_users = []
    users = User.query.all()
    for user in users:
        list_of_users.append(get_user(user))
    return jsonify(list_of_users)


@app.route('/users/<int:id>')
def show_one_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(get_user(user))
    return 'Пользователя с таким id нет в базе'


@app.route('/users', method=['POST'])
def add_user():
    data = request.json
    user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        age=data.get('age'),
        email=data.get('email'),
        role=data.get('role'),
        phone=data.get('phone')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(get_offer(user))


@app.route('/users/<int:id>/update', method=['PUT'])
def update_user_by_id(id):
    data = request.json
    user = User.query.get(id)
    user.first_name = data.first_name
    user.last_name = data.last_name
    user.age = data.age
    user.email = data.email
    user.role = data.role
    user.phone = data.phone
    db.session.commit()
    return f'Пользователь с id {id} обнавлен'


@app.route('/users/<int:id>/delete', method=['DELETE'])
def delete_user_by_id(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return f"Пользователь с id {id} удален"
    return f"Пользователя с id {id} нет в базе"


@app.route('/orders')
def show_all_orders():
    list_of_orders = []
    orders = Order.query.all()
    for order in orders:
        list_of_orders.append(get_order(order))
    return jsonify(list_of_orders)


@app.route('/orders/<int:id>')
def show_one_order(id):
    order = Order.query.get(id)
    if order:
        return jsonify(get_order(order))
    return 'Заказа с таким id нет в базе'


@app.route('/orders', method=['POST'])
def add_user():
    data = request.json
    order = Order(
        name=data.get('name'),
        description=data.get('description'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        address=data.get('address'),
        price=data.get('price'),
        customer_id=data.get('customer_id'),
        executor_id=data.get('executor_id')
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(get_offer(order))


@app.route('/orders/<int:id>/update', method=['PUT'])
def update_user_by_id(id):
    data = request.json
    order = Order.query.get(id)
    order.name = data.name
    order.description = data.description
    order.start_date = data.start_date
    order.end_date = data.end_date
    order.address = data.address
    order.price = data.price
    order.customer_id = data.customer_id
    order.executor_id = data.executor_id
    db.session.commit()
    return f'Товар с id {id} обновлен'


@app.route('/orders/<int:id>/delete', method=['DELETE'])
def delete_user_by_id(id):
    order = Order.query.get(id)
    if order:
        db.session.delete(order)
        db.session.commit()
        return f"Товар с id {id} удален"
    return f"Товара с id {id} нет в базе"


@app.route('/offers')
def show_all_offers():
    list_of_offers = []
    offers = Offer.query.all()
    for offer in offers:
        list_of_offers.append(get_offer(offer))
    return jsonify(list_of_offers)


@app.route('/offers/<int:id>')
def show_one_offer(id):
    offer = Offer.query.get(id)
    if offer:
        return jsonify(get_offer(offer))
    return 'Заказа с таким id нет в базе'


@app.route('/offers', method=['POST'])
def add_user():
    data = request.json
    offer = Order(
        order_id=data.get('order_id'),
        executor_id=data.get('executor_id'),
    )
    db.session.add(offer)
    db.session.commit()
    return jsonify(get_offer(offer))


@app.route('/offers/<int:id>/update', method=['PUT'])
def update_user_by_id(id):
    data = request.json
    offer = Order.query.get(id)
    offer.order_id = data.order_id
    offer.executor_id = data.executor_id
    return f'Заказ с id {id} обновлен'


@app.route('/offers/<int:id>/delete', method=['DELETE'])
def delete_user_by_id(id):
    offer = Order.query.get(id)
    if offer:
        db.session.delete(offer)
        db.session.commit()
        return f"Заказ с id {id} удален"
    return f"Заказа с id {id} нет в базе"


if __name__ == "__main__":
    app.run()
