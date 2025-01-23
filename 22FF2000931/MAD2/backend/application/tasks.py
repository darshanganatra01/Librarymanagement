from flask_mail import Message
from application.celery_tasker import FlaskTask  #celery_tasker
from main import celery_app #app mathi c_app
from application.mailer import mail
from application.models import *
from datetime import date,timedelta,datetime
from jinja2 import Template
import csv

@celery_app.task(base=FlaskTask)
def daily_mail():
    date_format = "%Y-%m-%d"

    all_issues = db.session.query(Bookissue).all()
    
    diff = [
        issue for issue in all_issues 
        if issue.rdate != "Not Defined" and (date.today() - datetime.strptime(issue.rdate, date_format).date()).days == -1
        and issue.status==2
    ]

    email_id=[]
    for i in diff:
        d=User.query.filter_by(uid=i.iuid).first()
        e=Book.query.filter_by(bid=i.ibid).first()
        email_id.append(d.email)

    email_rec = email_id
    email_subject = 'Return date approaching'
    email_body = 'hi,this msg is to let you know that return date for your book is approaching please return it before that' 

    msg = Message(subject=email_subject, recipients=email_rec, body=email_body)
    mail.send(msg)
    return 'ok'


@celery_app.task(base=FlaskTask)
def monthly_report():

    nouser=User.query.all()
    nobooks=Book.query.all()
    noassign=Bookissue.query.filter_by(status=2).all()
    nopending=Bookissue.query.filter_by(status=1).all()
    noreject=Bookissue.query.filter_by(status=0).all()
    nosecs=Section.query.all()

    reviews=Review.query.filter_by()

    from sqlalchemy import func

    def get_avg_reviews_for_book(book_id):
        avg_reviews = db.session.query(
            func.avg(Review.stars)
        ).filter(Review.rbid == book_id).scalar()
    
        return avg_reviews
    
    
    def get_avg_reviews_for_section(section_id):
        avg_reviews = db.session.query(
            func.avg(Review.stars)
        ).filter(Review.rsid == section_id).scalar()

        return avg_reviews
    
    ba={}
    for i in nobooks:
        ba[i.bid]=get_avg_reviews_for_book(i.bid)

    sa={}
    for i in nosecs:
        sa[i.sid]=get_avg_reviews_for_section(i.sid)
    
    

    def get_top_3_books():
        top_books = db.session.query(
            Book.bid, Book.bname, Book.author, Book.bdescription, Book.bdate, 
            func.avg(Review.stars).label('average_stars')
        ).join(Review, Book.bid == Review.rbid)\
        .group_by(Book.bid)\
        .order_by(func.avg(Review.stars).desc())\
        .limit(3)\
        .all()
    
        return top_books

    top_books=get_top_3_books()



    subject = 'Monthly Report'
    email_body = 'This is an monthly report.Please check the attachment'

    body = '''
    <html>
    <title>Monthly Report</title>
    <body>

    Hiii there
    <h3 Total number of Users : {{ nouser | length }}/>
    <h3 Total number of Books : {{ nobooks | length }}/>
    <h3 Total number of Issues : {{ noassign | length }}/>
    <h3 Total number of Sections : {{ nosecs | length }}/>
    <h3 Total number of Rejected Requests : {{ noreject | length }}/>
    <h3 Total number of Pending Requests : {{  nopending | length }}/>

    <h2>Section details</h2>
    <table border="2">
    <tr>
        <th>Section name</th>
        <th>Section Description</th>
        <th>Avg Reviews</th>
    </tr>
    {% for i in nosecs%}
    <tr>
        <td> {{i.sname}} </td>
        <td> {{i.description}} </td>
        <td> {{sa[i.sid]}}</td>
    <tr>
    {% endfor %}
    </table>

    <h2>Book details</h2>
    <table border="2">
    <tr>
        <th>Book name</th>
        <th>Author name</th>
        <th>Avg Reviews</th>
    </tr>
    {% for i in nobooks %}
    <tr>
        <td> {{i.bname}} </td>
        <td> {{i.author}} </td>
        <td> {{ba[i.bid]}}</td>
    <tr>
    {% endfor %}
    </table>

    <h2>Top3 Books</h2>
    <table border="2">
    <tr>
        <th>Book Name</th>
        <th>Author</th>
        <th>Avg Reviews</th>
    </tr>
    {% for i in top_books %}
    <tr>
        <td> {{i.bname}} </td>
        <td> {{i.author}} </td>
        <td>{{ba[i.bid]}}</td>
    </tr>
    {% endfor %}
    </table>

    </body>
    </html>
    '''

    template = Template(body)
    body = template.render(nosecs=nosecs,nouser=nouser,nobooks=nobooks,noassign=noassign,nopending=nopending,noreject=noreject,top_books=top_books,ba=ba,sa=sa)


    msg = Message(subject = subject, recipients=['adminapp@gmail.com'], body = email_body)
    msg.html = body
    mail.send(msg)

    return 'done'

@celery_app.task(ignore_result=False)
def create_csv():
    res = (db.session.query(
            User.name,
            Book.bname,
            Bookissue.idate,
            Bookissue.rdate
        )
        .join(Bookissue, User.uid == Bookissue.iuid)
        .join(Book, Bookissue.ibid == Book.bid)
    ).all()


    file_path = './static/file.csv'

    # Write the CSV file manually
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['User Name', 'Book Title', 'Date of Issue', 'Date of Return'])

        for r in res:
            csvwriter.writerow([r.name, r.bname, str(r.idate), str(r.rdate)])

    with open(file_path, 'r') as f:
        csv_data = f.read()

    subject = 'CSV File'
    body = 'Hi, Please check the attachment'
    msg = Message(subject=subject, recipients=['drashti@gmail.com'], body=body)
    msg.attach('file.csv', 'text/csv', csv_data)

    mail.send(msg)
    return file_path

@celery_app.task(base=FlaskTask)
def mail_report():
    return 'ok'