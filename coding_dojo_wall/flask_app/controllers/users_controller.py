from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import users
from flask_app.models import posts 
from flask_app.controllers import posts_controller
from datetime import datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/register', methods=["POST"])
def register():
    if not users.User.validate_registration(request.form):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['r_email']
        return redirect('/')
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["r_email"],
        "password": request.form["r_password"],
    }
    pw_hash = bcrypt.generate_password_hash(data['password'])
    data['password'] = pw_hash
    
    user_id = users.User.save(data)
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['r_email']
    session['user_id'] = user_id
    return redirect(f"/wall/{user_id}")
    
@app.route('/login', methods=["POST"])
def login():   
    user_in_db = users.User.get_user_by_email(request.form["l_email"])
    if not user_in_db:
        flash("Invalid Email", 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['l_password']):
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect(f"/wall/{session['user_id']}")

@app.route('/wall/<int:user_id>')
def success(user_id):
    if session:
        all_posts = posts.Post.get_all_posts()
        for post in all_posts:
            post.date.append(post.created_at.strftime('%m/%d/%Y'))
        return render_template("success.html", all_posts=all_posts)
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
