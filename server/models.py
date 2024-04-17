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
    def validating_name(self, key, author_name):
        if not author_name:
            raise ValueError('All authors should have a name')
        
        existing_author_name = Author.query.filter(Author.name == author_name).first()

        if existing_author_name:
            raise ValueError('An author with this name already exists')
        
        return author_name
        

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
    
    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if len(number) != 10 or not number.isdigit():
            raise ValueError('The phone number should be exactly 10 digits')
        
        return number

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('content', 'summary')
    def validate_content(self, key, string):
        if key == 'content':
            if len(string) < 250:
                raise ValueError('Post content length should be atleast 250 characters long')
        
        if key == 'summary':
            if len(string) > 250:
                raise ValueError('Post summary should be less than 250 characters long or equal to 250 characters long')
        return string
    
    @validates('category')
    def validate_category(self, key, category):
        if category != 'Fiction' or category != 'Non-Fiction':
            raise ValueError('The category should either be Fiction or Non-Fiction')
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError('Title is needed')
        
        clickbait_titles = ["Won't Believe", "Secret", "Top", "Guess"]

        for word in clickbait_titles:
            if word in title:
                return title
        raise ValueError("The title should have 'Won't Believe',  'Secret', 'Top', 'Guess'")

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
