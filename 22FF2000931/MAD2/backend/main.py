from flask import Flask,request,jsonify,make_response,send_from_directory
from application.config import Config
from application.database import db
from flask_security import Security, SQLAlchemyUserDatastore, current_user, roles_accepted, auth_token_required,verify_password,login_user
from application.models import *
from flask_cors import CORS
from datetime import date,timedelta,datetime
from application.mailer import mail
from flask_mail import Message
from celery import Celery
import flask_excel as excel
from sqlalchemy import func
import os
from application.caching import cache 
from sqlalchemy import desc
import matplotlib.pyplot as plt
import pandas as pd




user_datastore = SQLAlchemyUserDatastore(db, User, Role)

def make_celery(app):
    
    celery_app=Celery(app.name)
    celery_app.config_from_object("application.celeryconfig")
    app.extensions["celery"]=celery_app
    return celery_app


def make_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    security = Security(app, user_datastore)
    cache.init_app(app)
    mail.init_app(app)
    celery_app=make_celery(app)
    db.init_app(app)
    excel.init_excel(app)
    app.app_context().push()
    db.create_all()

    return app,celery_app

app,celery_app=make_app()
import application.tasks



with app.app_context():
    user_datastore.find_or_create_role(name="admin",description="admin of the app")
    user_datastore.find_or_create_role(name="user",description="user of the app")
    if not user_datastore.find_user(email="22f2000931@ds.study.iitm.ac.in"):
        user_datastore.create_user(name="darshan",email="22f2000931@ds.study.iitm.ac.in",state="gujarat",password="darshu12345",roles=["user"]) 
    if not user_datastore.find_user(email="adminapp@ds.study.iitm.ac.in"):
        user_datastore.create_user(name="admin",email="adminapp@ds.study.iitm.ac.in",state="private",password="siradmin01",roles=["admin"]) 
    db.session.commit()


@app.route('/testmail')
def celery_test():
    application.tasks.monthly_report.delay()
    return "mail sent"

from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'var1': {
        'task': 'application.tasks.daily_mail',
        'schedule': crontab(minute=00, hour=18)
    },

    'var2': {
        'task':'application.tasks.monthly_report',
        'schedule':crontab(minute=00,hour=9,day_of_month=1) 
    }
}


@app.route("/apilogin", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user :
        if verify_password(password, user.password):
            token = user.get_auth_token()
            return make_response({"token": token, "email": user.email,"role":user.roles[0].name}), 200
        else:
            return make_response({"message": "Password doesn't match"}), 402
    else:
        return make_response({"message": "User not present"}), 402




@app.route("/signup",methods=['GET','POST'])
def signup():
    data=request.get_json()
    name=data.get("name")
    email=data.get("email")
    state=data.get("state")    
    password=data.get("password")
    user=User.query.filter_by(email=email).first()
    
    if user:
        return make_response({"message":"User already exists!!!"}),402
    else:
        user_datastore.create_user(name=name,email=email,state=state,password=password,roles=["user"])
        db.session.commit()
        return make_response({"message":"Registered Successfully please login"}),201
    
    
@app.route("/liblogin", methods=["POST"])
def liblogin():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if user and any(i.name=="admin" for i in user.roles):
        if verify_password(password, user.password):
            token = user.get_auth_token()
            return make_response({"token": token, "email": user.email,"role":user.roles[0].name}), 200
        else:
            return make_response({"message": "Password doesn't match SIR!"}), 402
    else:
        return make_response({"message": "Invalid Credentials for Librarian"}), 402



@app.route("/addsection",methods=['GET','POST'])
@auth_token_required
@roles_accepted("admin")
def addsection():
    if request.method=="POST":
        data=request.get_json()
        name=data.get("name")
        date=data.get("date")
        description=data.get("description") 

        scheck=Section.query.filter_by(sname=name).first()

        if scheck:
            return make_response({"message":"Section already exists!!!"}),402
        else:
            add=Section(sname=name,sdate=date,description=description)
            db.session.add(add)
            db.session.commit()
            return make_response({"message":"Section Added Successfully"}),201
    else:
        slist=Section.query.all()
        rlist=[]
        for i in slist:
            dict={
            "sid":i.sid,
            "name":i.sname,
            "date":i.sdate,
            "description":i.description
            }
            rlist.append(dict)
        return make_response(rlist),200
    
@app.route("/editsection/<int:sid>",methods=['GET','POST'])
@auth_token_required
@roles_accepted("admin")
def editsection(sid):
    scheck=Section.query.filter_by(sid=sid).first()
    if request.method=="POST":
        data=request.get_json()
        name=data.get("name")
        date=data.get("date")
        description=data.get("description") 

        if scheck is None:
            return make_response({"message":"Section Doesn't exist!!!"}),402
        
        check2=Section.query.filter_by(sname=name).first()
        if check2 and name!=scheck.sname:
             return make_response({"message":"Please choose a different Section name!!"}),400

        
        
        else:
            scheck.sname=name
            scheck.sdate=date
            scheck.description=description
            db.session.commit()
            return make_response({"message":"Section Edited Successfully"}),201
    else:
        dict={
            "sid":scheck.sid,
            "name":scheck.sname,
            "date":scheck.sdate,
            "description":scheck.description
            }
        return make_response({"sec":dict}),200

    

@app.route("/sbooks/<int:sid>",methods=["GET","POST"])
@auth_token_required
@cache.cached(timeout=15)
def sbooks(sid):
    section=Section.query.filter_by(sid=sid).first()
    slist=section.books
    rlist=[]
    for i in slist:
            dict={
            "bid":i.bid,
            "bname":i.bname,
            "author":i.author,
            }
            rlist.append(dict)
    sec={
        "sname":section.sname,
        "description":section.description,
        "date":section.sdate
    }
    return make_response({"rlist":rlist,"sec":sec}),200


@app.route("/addbooks/<int:sid>",methods=["POST"])
@auth_token_required
@roles_accepted("admin")
def addbooks(sid):
        bookfile=request.files.get("bookfile")

        bname=request.form.get("bname")
        author=request.form.get("author")
        bdescription=request.form.get("bdescription")
        bdate=request.form.get("bdate")
        section=sid

        check=Book.query.filter_by(bname=bname).first()
        if check:
            return make_response({"message":"Book name already in use!!"}),402

        book=Book(bname=bname,bdescription=bdescription,author=author,bdate=bdate,section=section)
        db.session.add(book)
        db.session.commit()

        bookfile.save('../frontend/vue-project/src/assets/'+str(book.bid)+'.pdf')


        return make_response({"message":"Book added Successsfully!!"}),201



@app.route("/bookinfo/<bid>",methods=["GET"])
@auth_token_required
def bookinfo(bid):
    book=Book.query.get(bid)
    info={
        "bname":book.bname,
        "bdescription":book.bdescription,
        "author":book.author,
        "bdate":book.bdate,
        "sec":book.section
    }
    return make_response({"book":info}),200



@app.route("/openbook/<string:path>")
def openbook(path):
    return send_from_directory('../frontend/vue-project/src/assets/',path)



@app.route("/bstatus/<bid>",methods=["GET"])
@auth_token_required
def bstatus(bid):
    user=current_user
    if any(i.name=="user" for i in user.roles):
        status=Bookissue.query.filter_by(ibid=bid,iuid=user.uid).first()

        if status is None:
            msg={
                "iuid":-1,
                "iid":-1,
                "ibid":-1,
                "adate":"None",
                "idate":"None",
                "rdate":"None",
                "status":-1
            }    

        else:
            msg={
                "iuid":status.iuid,
                "iid":status.iid,
                "ibid":status.ibid,
                "idate":status.idate,
                "rdate":status.rdate,
                "adate":status.adate,
                "status":status.status
            }    
        
        return make_response({"bstatus":msg}),200
    
    elif any(i.name=="admin" for i in user.roles):
        s=Bookissue.query.filter_by(ibid=bid).all()
        slist=[]
        for i in s:
            user=User.query.filter_by(uid=i.iuid).first()
            username=user.name
            dict={
                "iuid":i.iuid,
                "iid":i.iid,
                "ibid":i.ibid,
                "adate":i.adate,
                "status":i.status,
                "username":username,
                "idate":i.idate,
                "rdate":i.rdate
            }
            slist.append(dict)

        return make_response({"bstatus":slist}),200
    

@app.route("/brequest/<bid>", methods=["GET"])
@auth_token_required
@roles_accepted("user")
def brequest(bid):
    user = current_user
    adate = date.today()
    check=Bookissue.query.filter_by(iuid=user.uid,status=2).all()
    if len(check)==5:
        return make_response({"message":"You can't request for more than 5 books!!"}),400
    
    add1=Bookissue.query.filter_by(iuid=user.uid, ibid=bid).first()
    if add1:
        add1.status=1
        db.session.commit()
        return make_response({"message":"Book request sent again!!"}),201
    else:
        add2 = Bookissue(iuid=user.uid, ibid=bid, adate=adate)
        db.session.add(add2)
        db.session.commit()
        return make_response({"message":"Book request sent!!"}),201



@app.route("/breturn/<bid>", methods=["GET"])
@auth_token_required
@roles_accepted("user")
def breturn(bid):
    user = current_user
    update=Bookissue.query.filter_by(ibid=bid,iuid=user.uid).first()
    db.session.delete(update)
    db.session.commit()
    return make_response({"message":"Book returned succesfully!!"}),201



@app.route("/brevoke/<bid>/<iuid>", methods=["GET"])
@auth_token_required
@roles_accepted("admin")
def brevoke(bid,iuid):
    revoke=Bookissue.query.filter_by(ibid=bid,iuid=iuid).first()
    db.session.delete(revoke)
    db.session.commit()
    return make_response({"message":"Book access has been revoked!!"}),201



@app.route("/baccept/<bid>/<iuid>", methods=["GET"])
@auth_token_required
@roles_accepted("admin")
def baccept(bid,iuid):
    check=Bookissue.query.filter_by(iuid=iuid,status=2).all()
    if len(check)==5:
        return make_response({"message":"User owns 5 books already!!"}),400
    accept=Bookissue.query.filter_by(ibid=bid,iuid=iuid).first()
    accept.status=2
    accept.idate=date.today()
    accept.rdate=date.today()+timedelta(days=7)
    db.session.commit()
    return make_response({"message":"Book request accepted!!"}),201



@app.route("/breject/<bid>/<iuid>", methods=["GET"])
@auth_token_required
@roles_accepted("admin")
def breject(bid,iuid):
    reject=Bookissue.query.filter_by(ibid=bid,iuid=iuid).first()
    reject.status=0
    db.session.commit()
    return make_response({"message":"Book request rejected!!"}),201


@app.route("/editbook/<int:bid>",methods=["GET","POST"])
@auth_token_required
@roles_accepted("admin")
def editbook(bid):
    if request.method=="POST":
        bookfile=request.files.get("bookfile")
        bname=request.form.get("bname")
        author=request.form.get("author")
        bdescription=request.form.get("bdescription")
        bdate=request.form.get("bdate")
        check=Book.query.filter_by(bid=bid).first()

        if check is None:
            return make_response({"message":"Book doesn't Exist!!"}),400
        
        check2=Book.query.filter_by(bname=bname).first()
        if check2 and bname!=check.bname:
             return make_response({"message":"Please choose a different bookname!!"}),400

        check.bname=bname
        check.author=author
        check.bdescription=bdescription
        check.bdate=bdate
        
        if bookfile:
            bookfile.save('../frontend/vue-project/src/assets/'+str(check.bid)+'.pdf')
        db.session.commit()

        return make_response({"message":"Book edited Successsfully!!"}),201
    

@app.route("/deletebook/<bid>")
@auth_token_required
@roles_accepted("admin")
def deletebook(bid):
    deli=Book.query.get(bid)
    ideli=Bookissue.query.filter_by(ibid=bid).delete()
    Review.query.filterby(rbid=bid).delete()
    db.session.delete(deli)
    db.session.commit()
    return make_response({"message":"Book deleted Successsfully!!"}),201


@app.route("/deletesec/<sid>")
@auth_token_required
@roles_accepted("admin")
def deletesec(sid):
    deli=Section.query.get(sid)
    books=deli.books

    for i in books:
        if os.path.exists('../frontend/vue-project/src/assets/'+str(i.bid)+'.pdf'):
            os.remove('../frontend/vue-project/src/assets/'+str(i.bid)+'.pdf')
        ideli=Bookissue.query.filter_by(ibid=i.bid).delete()
    for i in books:
        db.session.delete(i)

    Review.query.filterby(rsid=sid).delete()
    db.session.delete(deli)
    db.session.commit()
    return make_response({"message":"Section deleted Successsfully!!"}),201


@app.route("/search/<string:q>")
def search(q):
    q=q[0:len(q)-4]
    if (q is not None) and (q!="") and (q!=" "): 
        print(q)
        books = db.session.query(Book).filter(Book.bname.ilike(f'%{q}%')).all()
        sections = db.session.query(Section).filter(Section.sname.ilike(f'%{q}%')).all()
        authors=db.session.query(Book).filter(Book.author.ilike(f'%{q}%')).all()

        sbook=[]
        ssection=[]
        sauthor=[]

        for i in books:
            d={
                "bid":i.bid,
                "bname":i.bname,
            }
            sbook.append(d)

        for i in sections:
            d={
                "sid":i.sid,
                "sname":i.sname
            }
            ssection.append(d)

        for i in authors:
            d={
                "bid":i.bid,
                "author":i.author
            }
            sauthor.append(d)

        return make_response({"book":sbook,"section":ssection,"author":sauthor}),200
    return make_response({"book":[],"section":[],"author":[]}),200



@app.route("/breview/<bid>",methods=["GET","POST"])
@auth_token_required
def breview(bid):
    user=current_user
    if request.method=="POST":
        data=request.get_json()
        rev=data.get('review')
        check=Review.query.filter_by(ruid=user.uid,rbid=bid).first()
        if check:
            check.stars=int(rev)
            db.session.commit()
            return make_response({"message":"Review edited successfully!"}),201
        else:
            book=Book.query.filter_by(bid=bid).first()
            sec=book.sections.sid
            add=Review(ruid=user.uid,rsid=sec,rbid=bid,stars=int(rev))
            db.session.add(add)
            db.session.commit()
            return make_response({"message":"Review submitted successfully!"}),201
    else:
        check=Review.query.filter_by(ruid=user.uid,rbid=bid).first()
        if check:
            review={
                "rid":check.rid,
                "ruid":check.ruid,
                "rbid":check.rbid,
                "stars":check.stars
            }
        else:
             review={
                "rid":None,
                "ruid":None,
                "rbid":None,
                "stars":-1
            }
        
        return make_response(review),200


@app.route("/autorevoke")
def autorevoke():
    date_format = "%Y-%m-%d"

    all_issues = db.session.query(Bookissue).all()
    
    diff = [
        issue for issue in all_issues 
        if issue.rdate != "Not Defined" and (date.today() - datetime.strptime(issue.rdate, date_format).date()).days > 0
    ]
    
    if diff:
        book_ids = [issue.ibid for issue in diff]
        books_to_revoke = db.session.query(Book).filter(Book.bid.in_(book_ids)).all()
        book_names = [book.bname for book in books_to_revoke]
    
        for issue in diff:
            db.session.delete(issue)
        db.session.commit()
        
        str=""
        for i in book_names:
            str+=i+","
        return jsonify({"message": "Some of Your Books:" +str+ "has been revoked"}), 201
    else:
        return jsonify({"message": "No books to revoke"}), 200

    

@app.route("/secinfo",methods=["GET"])
def secinfo():
    sections=Section.query.all()
    top3_books = Book.query.order_by(desc(Book.bdate)).limit(3).all()
    sec=[]
    latestbooks=[]

    def get_avg_reviews_for_book(book_id):
        avg_reviews = db.session.query(
            func.avg(Review.stars)
        ).filter(Review.rbid == book_id).scalar()
    
        return avg_reviews
    
    for i in sections:
        dict={
               "sid":i.sid,
                "name":i.sname,
                "date":i.sdate,
                "description":i.description
                }
        sec.append(dict)
    
    for i in top3_books:
        dict2={
            "bid":i.bid,
            "bname":i.bname,
            "author":i.author,
            "bdate":i.bdate,
            "avgrev":get_avg_reviews_for_book(i.bid)
        }
        latestbooks.append(dict2)
    

    return make_response({"sec":sec,"latestbooks":latestbooks}),200


@app.route("/triggerexport", methods=["GET"])
@auth_token_required
@roles_accepted("admin")
def triggerexport():
    application.tasks.create_csv.delay()
    return make_response({"message":"You will get a mail soon!!"}),200


@app.route("/bookreview/<bid>")
@auth_token_required
def bookreview(bid):
    def get_avg_reviews_for_book(book_id):
        avg_reviews = db.session.query(
            func.avg(Review.stars)
        ).filter(Review.rbid == book_id).scalar()
    
        return avg_reviews
    avgrev=get_avg_reviews_for_book(bid)
    if avgrev:
        return make_response({"avgrev":avgrev}),200
    else:
        return make_response({"avgrev":"No reviews yet for this book"}),200
    

@app.route("/getprofile")
@auth_token_required
def getprofile():
    user=current_user
    abookissues=Bookissue.query.filter_by(iuid=user.uid,status=2).all()
    abooks=[]
    for i in abookissues:
        b={
            "bid":i.ibid,
            "bname":Book.query.filter_by(bid=i.ibid).first().bname,
            "author":Book.query.filter_by(bid=i.ibid).first().bname
        }
        abooks.append(b)

    pbookissues=Bookissue.query.filter_by(iuid=user.uid,status=1).all()
    pbooks=[]
    for i in pbookissues:
        b={
            "bid":i.ibid,
            "bname":Book.query.filter_by(bid=i.ibid).first().bname,
            "author":Book.query.filter_by(bid=i.ibid).first().bname
        }
        pbooks.append(b)
    
    cuser={
        "username":user.name,
        "email":user.email
    }

    return make_response({"abooks":abooks,"pbooks":pbooks,"cuser":cuser}),200


@app.route("/stats")
def stats():
    # Count total sections, books, and users
    totalsecs = db.session.query(Section).count()
    totalbooks = db.session.query(Book).count()
    totalusers = db.session.query(User).count()

    # Get top 3 books based on average review stars
    top_books = db.session.query(
        Book.bid,
        Book.bname,
        Book.author,
        func.avg(Review.stars).label('average_stars')
    ).join(Review, Book.bid == Review.rbid) \
    .group_by(Book.bid) \
    .order_by(func.avg(Review.stars).desc()) \
    .limit(3) \
    .all()

    # Prepare top books data
    topbooks = [
        {
            "bid": book.bid,
            "bname": book.bname,
            "author": book.author
        }
        for book in top_books
    ]

    # Save plots
    save_charts()

    # Create the response
    response = {
        "totalsecs": totalsecs,
        "totalbooks": totalbooks,
        "totalusers": totalusers,
        "topbooks": topbooks
    }

    return make_response(jsonify(response), 200)

def save_charts():
    # Data extraction for charts
    sections = db.session.query(Section).all()
    books = db.session.query(Book).all()
    requests = db.session.query(Bookissue).all()

    if sections and books and requests:
        section_book_count = {sec.sname: 0 for sec in sections}
        for book in books:
            section = db.session.query(Section).filter_by(sid=book.section).first()
            section_book_count[section.sname] += 1

        plt.figure(figsize=(10, 6))
        plt.pie(section_book_count.values(), labels=section_book_count.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Number of Books in Each Section')
        plt.savefig('../frontend/vue-project/src/assets/pie.png')
        plt.close()

        # 2. Line Graph: User Book Request Behavior
        data = {'date': [], 'requests': []}
        for req in requests:
            data['date'].append(req.adate)
            data['requests'].append(req.status)

        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.groupby('date').size()

        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df.values, marker='o', linestyle='-')
        plt.xlabel('Date')
        plt.ylabel('Number of Requests')
        plt.title('User Book Request Behavior Over Time')
        plt.grid(True)
        plt.savefig('../frontend/vue-project/src/assets/behaviour.png')
        plt.close()

    # 3. Histogram: Book Requests
        status_counts = [req.status for req in requests]

        if status_counts:
            plt.figure(figsize=(10, 6))
            plt.hist(status_counts, bins=range(4), edgecolor='black')
            plt.xlabel('Request Status')
            plt.ylabel('Frequency')
            plt.title('Histogram of Book Requests')
            plt.xticks([0, 1, 2], ['Rejected', 'Pending', 'Accepted'])
            plt.grid(True)
            plt.savefig('../frontend/vue-project/src/assets/histo.png')
            plt.close()

    # 4. Bar Chart: Number of Books per Author
    author_book_count = {}
    for book in books:
        author_book_count[book.author] = author_book_count.get(book.author, 0) + 1
    
    if author_book_count:

        plt.figure(figsize=(12, 8))
        plt.barh(list(author_book_count.keys()), author_book_count.values(), color='skyblue')
        plt.xlabel('Number of Books')
        plt.title('Number of Books per Author')
        plt.gca().invert_yaxis()
        plt.grid(axis='x')
        plt.savefig('../frontend/vue-project/src/assets/bar.png')
        plt.close()

if __name__ == '__main__':
    app.run(debug=True)





#sresults(books:[{}],sections:[{}],authors:[{}])