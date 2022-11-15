from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*[0-9]$)(?=.*[a-zA-Z])')

class User:
    db = "login_registration_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {
            "email": data
        }
        result = connectToMySQL(cls.db).query_db(query, data)
        if result == False or len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() , NOW() );"
        result = connectToMySQL(cls.db).query_db( query, data )
        return result
    
    @staticmethod
    def validate_registration(data):
        reg_is_valid = True
        email_is_valid = True
        if len(data['first_name']) < 2:
            flash("First Name must be at least 2 characters.", 'registration')
            reg_is_valid = False
        if not data['first_name'].isalpha():
            flash("First Name must use letters only.", 'registration')
            reg_is_valid = False
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 2 characters.", 'registration')
            reg_is_valid = False
        if not data['last_name'].isalpha():
            flash("Last Name must use letters only.", 'registration')
            reg_is_valid = False
        if not EMAIL_REGEX.match(data['r_email']): 
            flash("Invalid email address!", 'registration')
            reg_is_valid = False
            email_is_valid = True
        if email_is_valid:
            email_in_db = User.get_user_by_email(data["r_email"])
            if email_in_db:
                flash("Email is already in use! Please log in.", "registration")
                reg_is_valid = False
        if not PASSWORD_REGEX.match(data['r_password']):
            flash("Password must contain at least one letter and one number.", 'registration')
            reg_is_valid = False
        if len(data['r_password']) < 8:
            flash("Password must be at least 8 characters.", 'registration')
            reg_is_valid = False
        if data["r_password"] != data["confirm_password"]:
            flash("Passwords do not match!", 'registration')
            reg_is_valid = False
        return reg_is_valid
