from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Post:
    def __init__(self, data):
        self.id = data['posts.id']
        self.content = data['content']
        self.created_at = data['posts.created_at']
        self.updated_at = data['posts.updated_at']
        self.user_id = data['user_id']
        self.user_first_name = data['first_name']
        self.date = []
    
    @classmethod
    def get_all_posts(cls):
        query = "SELECT * FROM users JOIN posts ON users.id = posts.user_id ORDER BY posts.created_at DESC;"
        results = connectToMySQL('cd_wall_schema').query_db(query)
        posts = []
        for post in results:
            print(post['created_at'])
            posts.append(cls(post))
        return posts
    
    @classmethod
    def create_post(cls,data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s,%(user_id)s);"
        data = {
            "content": data["content"],
            "user_id": data["user_id"]
        }
        result = connectToMySQL('cd_wall_schema').query_db(query, data)
        return result
    
    @classmethod
    def delete_post(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        data = {
            "id": data
        }
        result = connectToMySQL('cd_wall_schema').query_db(query, data)
        return result
    
    @staticmethod
    def validate_post(data):
        is_valid = True
        if not data:
            flash("Post content must not be blank", 'post')
            is_valid = False
        return is_valid