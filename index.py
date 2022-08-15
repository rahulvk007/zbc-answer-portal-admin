import datetime

from flask import Flask, render_template, session, request, redirect

import flask_admin as admin
from flask_mongoengine import MongoEngine
from flask_admin.form import rules
from flask_admin.contrib.mongoengine import ModelView



from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://rahulvk:rvk4551@cluster0.c8dkc.mongodb.net/?retryWrites=true&w=majority")

db = cluster["answer-portal"]
user_collection = db["users"]


# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'
app.config['MONGODB_SETTINGS'] = {
    'host':'mongodb+srv://rahulvk:rvk4551@cluster0.c8dkc.mongodb.net/answer-portal?retryWrites=true&w=majority'
}


db = MongoEngine()
db.init_app(app)


# Define mongoengine documents
class Users(db.Document):
    email = db.EmailField()
    name = db.StringField(max_length=40)
    password = db.StringField(max_length=40)
    answer_status = db.BooleanField()
    score = db.IntField()
    def __unicode__(self):
        return self.name

class Answers(db.Document):
    answers = db.StringField(max_length=200)



class MyModelView(ModelView):
    def is_accessible(self):
        if 'name' in session:
            h = user_collection.find_one({"name": session['name']})
            if h:
                return True
            else:
                return False



# Flask views
@app.route('/', methods=['POST','GET'])
def index():
    if 'name' in session:
        h = user_collection.find_one({"name": session['name']})
        if h:
            return redirect('/admin/')
    if request.method == "POST":
        details = request.form
        name = details["username"]
        password = details["passwd"]
        lg = user_collection.find_one({"name": name})
        if lg:
            if name == lg['name'] and password == lg['password'] and name == 'admin':
                session['name'] = name
        if 'name' in session:
            if session['name'] == name:
                return redirect('/admin/')
    return render_template('login.html')



app.secret_key = 'supersecret'


admin = admin.Admin(app, 'ZBC Answer Portal')

    # Add views
admin.add_view(MyModelView(Users))
admin.add_view(MyModelView(Answers))
    # Start app

