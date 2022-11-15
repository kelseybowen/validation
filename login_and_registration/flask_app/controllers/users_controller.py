from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/register', methods=["POST"])
def register():
    if not User.validate_registration(request.form):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['r_email']
        return redirect('/')
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["r_email"],
        "password": bcrypt.generate_password_hash(request.form["r_password"])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/success')
    
@app.route('/login', methods=["POST"])
def login():
    user_in_db = User.get_user_by_email(request.form["l_email"])
    if not user_in_db:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['l_password']):
        flash("Invalid Password", 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/success')

@app.route('/success')
def success():
    if session:
        return render_template("success.html")
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
