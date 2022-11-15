from flask_app.models.order import Order
from flask_app import app
from flask import render_template, request, redirect, session

@app.route('/')
def index():
    session.clear()
    return redirect('/cookies')

@app.route('/cookies')
def show_all_orders():
    all_orders = Order.get_all_orders()
    return render_template("cookies.html", all_orders=all_orders)

@app.route('/cookies/edit/<int:id>')
def edit_order(id):
    order = Order.get_one_order(id)
    if "customer_name" not in session:
        session["customer_name"] = order.customer_name
    if "cookie_type" not in session:
        session["cookie_type"] = order.cookie_type
    if "num_of_boxes" not in session:
        session["num_of_boxes"] = order.num_of_boxes
    return render_template("edit_order.html", order=order)

@app.route('/update_order/<int:id>', methods=["POST"])
def update_order(id):
    data = {
            "id": id,
            "customer_name": request.form['customer_name'],
            "cookie_type": request.form['cookie_type'],
            "num_of_boxes": request.form['num_of_boxes'],
        }
    if not Order.validate_order(data):
        return redirect(f"/cookies/edit/{data['id']}")
    Order.update_order(data)
    session.clear()
    return redirect('/cookies')

@app.route('/new_order')
def new_order():
    return render_template("new_order.html")
    
@app.route('/log_new_order', methods=["POST"])
def log_new_order():
    data = {
            "customer_name": request.form['customer_name'],
            "cookie_type": request.form['cookie_type'],
            "num_of_boxes": request.form['num_of_boxes']
        }
    if "customer_name" not in session:
        session["customer_name"] = data["customer_name"]
    if "cookie_type" not in session:
        session["cookie_type"] = data["cookie_type"]
    if "num_of_boxes" not in session:
        session["num_of_boxes"] = data["num_of_boxes"]
    # return render_template("edit_order.html", order=order)
    if not Order.validate_order(data):  
        # session_data = {
        #     session["customer_name"]: request.form['customer_name'],
        #     session["cookie_type"]: request.form['cookie_type'],
        #     session["num_of_boxes"]: request.form['num_of_boxes']
        # }
        return redirect('/new_order')
    Order.new_order(data)
    return redirect('/cookies')