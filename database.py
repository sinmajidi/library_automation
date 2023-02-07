from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
app.config['SECRET_KEY']='jhvhijghlkbvhjvjkjhvcj'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
class Librarian(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.Text)
    password = db.Column(db.Text)
    def __repr__(self):
        return f'acant({self.username},{self.password})'
class Students(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    student_name = db.Column(db.Text)
    student_family = db.Column(db.Text)
    student_id_code = db.Column(db.Text)
    student_number=db.Column(db.Text)
    student_phone = db.Column(db.Text)
    student_parent_phone = db.Column(db.Text)
    home_phone = db.Column(db.Text)

    # borrowed_book=db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

    def __repr__(self):
        return f'student({self.id},{self.student_name},{self.student_family},{self.student_id_code},{self.student_number})'
class Books(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    book_topic=db.Column(db.Text)
    book_code = db.Column(db.Text)
    # does = db.relationship('Students', backref='brrower', lazy=True)
    def __repr__(self):
        return f'book({self.id},{self.book_topic},{self.book_code})'

class borrow(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    book_topic=db.Column(db.Text)
    book_code = db.Column(db.Text)
    student_name=db.Column(db.Text)
    student_family = db.Column(db.Text)
    student_number = db.Column(db.Text)
    first_date_of_borrow=db.Column(db.Text)
    second_date_of_borrow=db.Column(db.Text)
    number_of_extention=db.Column(db.Integer)
    librarian = db.Column(db.Text)
    def __repr__(self):
        return f'borrow({self.id},{self.book_topic},{self.book_code},{self.student_name},{self.student_family},{self.student_number})'

class Borrow_history(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_topic = db.Column(db.Text)
    book_code = db.Column(db.Text)
    student_name = db.Column(db.Text)
    student_family = db.Column(db.Text)
    student_number = db.Column(db.Text)
    date_of_borrow = db.Column(db.Text)
    date_of_back = db.Column(db.Text)
    number_of_extention = db.Column(db.Integer)
    librarian = db.Column(db.Text)

    def __repr__(self):
        return f'borrow({self.id},{self.book_topic},{self.book_code},{self.student_name},{self.student_family},{self.student_number})'
