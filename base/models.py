# from django.db import models

# Create your models here.
from email.policy import default
from enum import unique
from mongoengine import Document, fields

class StudentDetails(Document):
    firstname = fields.StringField(max_length = 255)
    lastname = fields.StringField(max_length = 255)
    rollno = fields.IntField(unique=True)
    email = fields.EmailField(max_length = 255, unique=True)
    username = fields.StringField(max_length = 255)
    password = fields.StringField(max_length = 255)
    confirm_password = fields.StringField(max_length = 255)

    def to_json(self):
        return {
            "rollno" : self.rollno,
            "firstname" : self.firstname,
            "lastname" : self.lastname,
            "email_id" : self.email,
            "password" : self.password
        }

class LibrarianDetails(Document):
    firstname = fields.StringField(max_length = 255)
    lastname = fields.StringField(max_length = 255)
    empid = fields.StringField(max_length = 255, unique=True)
    email = fields.EmailField(max_length = 255, unique=True)
    username = fields.StringField(max_length = 255)
    password = fields.StringField(max_length = 255)
    confirm_password = fields.StringField(max_length = 255)

    def to_json(self):
        return {
            "empid" : self.empid,
            "firstname" : self.firstname,
            "lastname" : self.lastname,
            "email_id" : self.email,
            "password" : self.password
        }

class BookDetails(Document):
    bookid = fields.IntField(unique=True) 
    bookname = fields.StringField(max_length = 255)
    author = fields.StringField(max_length = 255)
    summary = fields.StringField()
    bookimage = fields.StringField()
    noofcopies = fields.IntField()

    def to_json(self):
        return {
            "bookid" : self.bookid,
            "bookname" : self.bookname,
            "author" : self.author,
            "summary" : self.summary,
            "bookimage" : self.bookimage,
            "noofcopies" : self.noofcopies
        }

class BookLendings(Document):
    bookid = fields.IntField()
    rollno = fields.IntField()
    pending =fields.IntField(default = 1)
    approved = fields.IntField(default = 0)
    requesteddate = fields.StringField()

    def to_json(self):
        return {
            "bookid" : self.bookid,
            "rollno" : self.rollno,
            "pending" : self.pending,
            "approved" : self.approved,
            "requesteddate" : self.requesteddate
        }




