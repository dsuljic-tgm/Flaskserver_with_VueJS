from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_cors import CORS


# Flaskapp wird erstellt
app = Flask(__name__)
# Flaskrestful: Application wird erstellt
api = Api(app)
# persistente Datenbank.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
# Datenbank wird erstellt
db = SQLAlchemy(app)
CORS(app)

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

#Datenbank wird erstellt
db.create_all()

#db.session.add(User(username="Admin", email="admin@admin.com", password="password"))
#db.session.commit()

db.session.add(Message(text="Hallo Welt", owner=1))
db.session.commit()


def check_auth(username, password):
    return username == 'admin' and password == 'admin'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# Resource, weil Flaskrestful ein Objekt auf eine Route binden muss. Dieses Objekt
# beinhlatet die HTTP-Methoden, die auf dieser Resource verwendet werden können und diese in dieser Klasse implementiert.
class UseResource(Resource):

    # Die Methoden MÜSSEN GET POST DELETE UND PUT heißen !!!
    # POST = ADD
    #@requires_auth
    def post(self):
        # Übersetzer: von Request zu Python übersetzt
        parser = reqparse.RequestParser()
        # Die Argumente username und email müssen vorhanden sein
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        # Fügt das Objekt in die Datenbank hinzu
        db.session.add(User(username=parser.parse_args().username, email=parser.parse_args().email, password=parser.parse_args().password))
        db.session.commit()
        # Returned etwas
        return 'success', 200

    #@requires_auth
    def get(self):
        # rto = return Object, json array
        rto = []
        # iterriert durch alle Userobjekte, weil User.query.all() nicht JSON-Serializable ist.
        # Flask braucht etwas in Json, bzw. etwas was in Json umgewandelt werden kann
        for element in User.query.all():
            # fügt alle Atribute vom User in ein neues Objekt, welches in das returnobjectliste hinzugefügt wird.
            rto.append({
                "id": element.id,
                "username": element.username,
                "email": element.email,
                "password": element.password
            })
        return rto

    #@requires_auth
    def delete(self):
        parser = reqparse.RequestParser()
        # Die ID muss vorhanden sein /Siehe Insomnia JS
        parser.add_argument('id', type=int)
        # Übersetzt HTTP-Argumente in Python-Variable
        id = parser.parse_args().id

        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return 'successfully deleted', 200

    #@requires_auth
    def put(self):
        # Übersetzer: von Request zu Python übersetzt
        parser = reqparse.RequestParser()
        # ID muss vorhanden sein bei dem Request
        parser.add_argument('id', type=int)
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
        # Übersetzt HTTP-Argumente in Python-Variable
        id = parser.parse_args().id

        # Der User, welcher geändert werden soll wird durch die id definiert
        user = User.query.get(id)
        # username soll geändert werden
        username=parser.parse_args().username
        # email soll geändert werden
        email = parser.parse_args().email
        # password soll geändert werden
        password = parser.parse_args().password

        # derzeitiger username und derzeitige email wird ersetzt
        user.username=username
        user.email=email
        user.password=password

        db.session.commit()
        return 'successfully updated', 200



# ========================================
# ================Messages================
# ========================================
class UseResourceMessages(Resource):
    def post(self):
        # Übersetzer: von Request zu Python übersetzt
        parser = reqparse.RequestParser()
        # Die Argumente username und email müssen vorhanden sein
        parser.add_argument('text', type=str)
        parser.add_argument('owner', type=int)
        # Fügt das Objekt in die Datenbank hinzu
        db.session.add(Message(text=parser.parse_args().text,owner=parser.parse_args().owner))
        db.session.commit()
        # Returned etwas
        return 'success', 200

    #@requires_auth
    def get(self):
        # rto = return Object, json array
        rto = []
        # iterriert durch alle Userobjekte, weil User.query.all() nicht JSON-Serializable ist.
        # Flask braucht etwas in Json, bzw. etwas was in Json umgewandelt werden kann
        for element in Message.query.all():
            # fügt alle Atribute vom User in ein neues Objekt, welches in das returnobjectliste hinzugefügt wird.
            rto.append({
                "messageID": element.messageID,
                "text": element.text,
                "owner": element.owner
            })
        return rto

class UseResourceMessage(Resource):

    #@requires_auth
    # Hier wird die messageID über die URL mitgegeben
    def delete(self, messageID):
        message = Message.query.get(messageID)
        db.session.delete(message)
        db.session.commit()
        return 'successfully deleted', 200

    #@requires_auth
    # Hier wird die messageID über die URL mitgegeben
    def put(self, messageID):
        # Übersetzer: von Request zu Python übersetzt
        parser = reqparse.RequestParser()
        # ID muss vorhanden sein bei dem Request
        parser.add_argument('text', type=str)
        parser.add_argument('owner', type=str)
        # Übersetzt HTTP-Argumente in Python-Variable

        # Der User, welcher geändert werden soll wird durch die id definiert
        message = Message.query.get(messageID)
        # username soll geändert werden
        text=parser.add_argument().text
        # email soll geändert werden
        owner = parser.add_argument().owner


        # derzeitiger username und derzeitige email wird ersetzt
        message.text=text
        message.owner=owner

        db.session.commit()
        return 'successfully updated', 200


# Hier wird der Pfad erstellt, wo diese Resource zur Verfügung gestellt wird.
api.add_resource(UseResource, '/')
api.add_resource(UseResourceMessages, '/chat')
api.add_resource(UseResourceMessage, '/chat/<string:messageID>') #messageID als Teil der URL

# Wenn main-Thread ausgeführt wird die Flask-App mit Werkzeug ausgeführt. Werkzeug ist nicht für ein öffentliches Deployment empfohlen.
if __name__ == '__main__':
    app.run(debug=True)