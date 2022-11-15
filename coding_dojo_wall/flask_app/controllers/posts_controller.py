from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import users
from flask_app.models import posts
from datetime import datetime

@app.route('/publish_post', methods=["POST"])
def publish_post():
    if session:
        data = {
            "content": request.form["new_post"],
            "user_id": session["user_id"]
        }
        if not posts.Post.validate_post(data["content"]):
            return redirect(f"/wall/{data['user_id']}")
        posts.Post.create_post(data)
    return redirect(f"/wall/{data['user_id']}")

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    if session:
        posts.Post.delete_post(post_id)
        return redirect(f"/wall/{session['user_id']}")
    else:
        return redirect('/')