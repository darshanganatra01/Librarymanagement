from application.database import db
from flask_security import UserMixin, RoleMixin


class User(db.Model,UserMixin):
    uid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    state=db.Column(db.String)
    password=db.Column(db.String,nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255),unique=True)
    active = db.Column(db.Boolean())

    roles = db.relationship('Role',secondary='role_user',backref=db.backref('users',lazy=True))



class Role(db.Model,RoleMixin):
    rid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,unique=True,nullable=True)
    description=db.Column(db.String,nullable=False)
    


class RoleUser(db.Model):
    ruid = db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.Integer,db.ForeignKey(User.uid),nullable=False)
    rid=db.Column(db.Integer,db.ForeignKey(Role.rid),nullable=False)


class Section(db.Model):
    sid=db.Column(db.Integer,primary_key=True)
    sdate=db.Column(db.String,nullable=False)
    sname=db.Column(db.Integer,unique=True,nullable=False)
    description=db.Column(db.String)


class Book(db.Model):
    bid=db.Column(db.Integer,primary_key=True)
    bname=db.Column(db.String,unique=True,nullable=False)
    author=db.Column(db.String,nullable=False)
    bdescription=db.Column(db.String)
    bdate=db.Column(db.String,nullable=False)
    section=db.Column(db.Integer,db.ForeignKey(Section.sid),nullable=False)

    sections=db.relationship('Section',backref='books')


class Review(db.Model):
    rid=db.Column(db.Integer,primary_key=True)
    rbid=db.Column(db.Integer,db.ForeignKey(Book.bid),nullable=False)
    ruid=db.Column(db.Integer,db.ForeignKey(User.uid),nullable=False)
    stars=db.Column(db.Integer,nullable=False)
    rsid=db.Column(db.Integer,db.ForeignKey(Section.sid),nullable=False)


class Bookissue(db.Model):
    iid=db.Column(db.Integer,primary_key=True)
    ibid=db.Column(db.Integer,db.ForeignKey(Book.bid),nullable=False)
    iuid=db.Column(db.Integer,db.ForeignKey(User.uid),nullable=False)
    adate=db.Column(db.String)
    idate=db.Column(db.String,default="Not issued")
    rdate=db.Column(db.String,default="Not Defined")
    status=db.Column(db.Integer,default=1,nullable=False)
    #0 rejected
    #1 pending
    #2 accepted











