def get_user(user):
    return {'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'email': user.email,
            'role': user.role,
            'phone': user.phone
            }


def get_order(order):
    return {
        'name': order.name,
        'description': order.description,
        'start_date': order.start_date,
        'end_date': order.end_date,
        'address': order.address,
        'price': order.price,
        'customer_id': order.customer_id,
        'executor_id': order.executor_id
    }


def get_offer(offer):
    return {
        'order_id': offer.order_id,
        'executor_id': offer.executor_id
    }
