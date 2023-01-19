
import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:123456@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)



class User(db.Model):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    categoryuse = db.Column(db.String(100), default="individual")
    urlid = db.Column(db.String(64), index = True, unique = True, nullable = True)
    following = db.relationship(
        'User', lambda: user_following,
        primaryjoin=lambda: User.id == user_following.c.user_id,
        secondaryjoin=lambda: User.id == user_following.c.following_id,
        backref='followers'
    )
    products=db.relationship("Product")

    def __init__(self, id,urlid,username,followers=[]):
        self.id=id
        self.username=username
        self.urlid = urlid
        self.followers=followers
    def __str__(self) -> str:
        return self.username

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey('users.urlid'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    category = db.Column(db.String(400), nullable=False)
    text = db.Column(db.Text, nullable=False)
    title=db.Column(db.String(400), nullable=False)
    def __init__(self, id,title, text,category):
        self.id =id
        self.title = title
        self.text = text
        self.category=category
    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"

## this will create an association table called user_following
user_following = db.Table(
    'user_following', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True),
    db.Column('following_id', db.Integer, db.ForeignKey(User.id), primary_key=True)
)

@app.route("/")
def home():
  with app.app_context():
    db.create_all()
  return "Hello, Flask!"


@app.route("/do")
def do():
    db.create_all()
    tom=User(1,"1","tom")
    flask=User(2,"2","flask")
    off=User(3,"3","off")
    PS=User(4,"4","PS")
    sub=User(5,"5","sub")
    qew=User(6,"6","qew")
    Jan=User(7,"7","Jan")
    db.session.add(tom)
    db.session.commit()
    db.session.add(flask)
    db.session.commit()
    db.session.add(off)
    db.session.commit()
    db.session.add(PS)
    db.session.commit()
    db.session.add(sub)
    db.session.commit()
    db.session.add(qew)
    db.session.commit()
    # result=db.session.add_all([tom, flask, off,PS,sub,qew,Jan])
    return "sucess"
@app.route("/q")
def query():
    user = User.query.filter_by(id=15).first()
    print(user)
    # get followers 
    print (user.followers)
    # get followings
    print(user.followers[0].following)
    user1=User.query.filter_by(id=2).first()
    print(type(user1))
    print(type(user.followers))
    # add followers
    user.followers.append(user1)
    print(user.followers)
    db.session.add(user)
    db.session.commit()
    return "1"


@app.route("/add")
def add():
    u2 = User(12,12,username='jacob1')
    u3 = User(13,13,username='james2')
    u4 = User(14,14,username='victor3')
    u1 = User(15,15,username='david4', followers=[u2, u3, u4])
    db.session.add_all([u1,u2,u3,u4])
    db.session.commit()
    return "1"



@app.route('/products', methods=['GET','POST'])
def addproduct():
    if request.method == 'POST':
        companyId = request.form.get('companyId')
        title = request.form.get('title')
        text=request.form.get('text')
        category=request.form.get('category')
        p1 = Product(id=6,title=title,text=text,category=category)
        user1 = User.query.filter_by(id=companyId).first()
        user1.products.append(p1)
        db.session.add(user1)
        db.session.commit()
        # print(url_for("addproduct")+"?id="+str(user1.id))
        return redirect(url_for("addproduct")+"?id="+str(user1.id))
    target_id=request.args.get("id")
    print(target_id)
    target_company=User.query.filter_by(id=target_id).first()
    products=Product.query.filter_by(user_id=str(target_company.id)).order_by(Product.date.desc())
    most_recent=products[0]
    categories = set()
    for p in products:
        print(p)
        categories.add(p.category)
    print(categories)
    return render_template('products2.html', most_recent=most_recent,company=target_company, products=products,categories=categories)
    