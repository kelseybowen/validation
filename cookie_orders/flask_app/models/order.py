from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Order:
    def __init__(self, data):
        self.id = data['id']
        self.customer_name = data['customer_name']
        self.cookie_type = data['cookie_type']
        self.num_of_boxes = data['num_of_boxes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all_orders(cls):
        query = "SELECT * FROM orders;"
        results = connectToMySQL('cookies_schema').query_db(query)
        orders = []
        for order in results:
            orders.append(cls(order))
        return orders
    
    @classmethod
    def get_one_order(cls, id):
        query = "SELECT * FROM orders WHERE id = %(id)s;"
        data = {
            "id": id
            }
        result = connectToMySQL('cookies_schema').query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def update_order(cls, data):
        query = "UPDATE orders SET customer_name = (%(customer_name)s), cookie_type = (%(cookie_type)s), num_of_boxes = (%(num_of_boxes)s), updated_at = NOW() WHERE id = (%(id)s);"
        order_data = {
            "id": data['id'],
            "customer_name": data['customer_name'],
            "cookie_type": data['cookie_type'],
            "num_of_boxes": data['num_of_boxes'],
        }
        return connectToMySQL('cookies_schema').query_db(query, order_data)
    
    @classmethod
    def new_order(cls, data):
        query = "INSERT INTO orders ( customer_name, cookie_type, num_of_boxes, created_at ) VALUES ( %(customer_name)s , %(cookie_type)s , %(num_of_boxes)s, NOW() );"
        return connectToMySQL('cookies_schema').query_db(query, data)
    
    @staticmethod
    def validate_order(order):
        is_valid = True
        if len(order['customer_name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if not order['customer_name'].isalpha():
            flash("Name must use valid characters.")
        if len(order['cookie_type']) < 3:
            flash("Cookie Type must be at least 3 characters.")
            is_valid = False
        if not order['cookie_type'].isalpha():
            flash("Cookie Type must use valid characters.")
        if int(order['num_of_boxes']) < 1:
            flash("Number of Boxes cannot be less than 1.")
            is_valid = False
        return is_valid