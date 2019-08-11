from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

# Flaskapp wird erstellt
app = Flask(__name__)
# Authentication
auth = HTTPBasicAuth()
# Flaskrestful: Application wird erstellt
api = Api(app)
# persistente Datenbank.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
# Datenbank wird erstellt
db = SQLAlchemy(app)
# Cross origin resource sharing = Wer hat rechte und wer nicht? Accesssystem. Egal wer, darf draif zugreifen
CORS(app)

# Dem Authklasse das ist die Methode, welche beim authentizieren aufgerufen wird
@auth.verify_password
def verify_password(username, password):
    # Holt den Username wieder mit Username und checked ob das passwort richtig ist.
    #return User.query.filter_by(username=username).first().password == password
    return True

# Konstrukt der Resource
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(15), unique=False, nullable=False)

class Message(db.Model):
    messageID = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), unique=False,nullable=False)
    owner = db.Column(db.Integer, unique=False, nullable=False)
    forumPost = db.Column(db.ForeignKey('forumpost.postID'), unique=False)  # db.ARRAY(Message)

class Forumpost(db.Model):
    postID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    text = db.Column(db.String, unique=False)

#Datenbank wird erstellt
db.drop_all()
db.create_all()

db.session.add(User(username="Admin", email="admin@admin.com", password="password"))
db.session.commit()

db.session.add(Forumpost(title="Hallo Welt", text = "Ich bin neu hier"))
db.session.commit()

db.session.add(Message(text="Hallo Welt", owner=1, forumPost=1))
db.session.commit()



from user import UseResourceUsers, UseResourceUsersUI
from login import Login
from message import UseResourceMessagesUI, UseResourceMessages
from forumPost import UseResourceForumPosts, UseResourceForumPostsUI




# Hier wird der Pfad erstellt, wo diese Resource zur Verfügung gestellt wird.
api.add_resource(UseResourceUsers, '/users')
api.add_resource(UseResourceUsersUI, '/users/<id>')
api.add_resource(UseResourceMessages, '/chat')
api.add_resource(UseResourceMessagesUI, '/chat/<messageID>')
api.add_resource(UseResourceForumPosts, '/posts')
api.add_resource(UseResourceForumPostsUI, '/posts/<postID>')
api.add_resource(Login, '/login')
# Wenn main-Thread ausgeführt wird die Flask-App mit Werkzeug ausgeführt. Werkzeug ist nicht für ein öffentliches Deployment empfohlen.
if __name__ == '__main__':
    app.run(debug=True)