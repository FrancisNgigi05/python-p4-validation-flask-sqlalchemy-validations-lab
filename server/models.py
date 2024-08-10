from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, author_name):
        if not author_name:
            raise ValueError('There should be a name')
        
        existing_name = Author.query.filter(Author.name == author_name).first()

        if existing_name:
            raise ValueError('The author name already exists') 
        return author_name
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError('requires each phone number to be exactly ten digit.')
        return number

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, db.CheckConstraint('len(content) >= 250'))
    category = db.Column(db.String)
    summary = db.Column(db.String, db.CheckConstraint('len(summary) <= 250'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('content', 'summary')
    def validat_content_length(self, key, string):
        if key == 'content':
            if len(string) < 250:
                    raise ValueError('Post content length should be atleast 250 characters long')
        
        if key == 'summary':
            if len(string) > 250:
                raise ValueError('Post summary should be less than 250 characters long or equal to 250 characters long')
        return string
    @validates('category')
    def validate_category(self, key, category):
        if category != "Fiction" and category != "Non-Fiction":
            raise ValueError("The category should be either Fiction or Non-Fiction")
        return category
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Title is needed')

        click_bait = ["Won't Believe", "Secret", "Top", "Guess"]

        if not any(word in title for word in click_bait):
            raise ValueError("The title must contain at least one of the following phrases: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
    
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'