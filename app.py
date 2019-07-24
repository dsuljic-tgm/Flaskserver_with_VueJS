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
CORS(app)

@auth.verify_password
def verify_password(username, password):
    # Holt den Username wieder mit Username und checked ob das passwort richtig ist.
    return User.query.filter_by(username=username).first().password == password
    #return True

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

#db.session.add(Message(text="Hallo Welt", owner=1))
#db.session.commit()

class Login(Resource):

    def get(self):
        # Verifizieren von Username und Passwort in Frontend
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)

        # Gibt den User zurück. Holt in mit dem Username, statt mit der ID
        user = User.query.filter_by(username = parser.parse_args().username).first()

        if user == None:
            return 'Username not found, please try again.', 401
        #parser.parse_args() = das aktuell eingegebene Passwort
        elif user.password == parser.parse_args().password:
            # returned die UserID des Users
            return user.id
        else:
            return 'Wrong password, please try again', 402

        # iterriert durch alle Userobjekte, weil User.query.all() nicht JSON-Serializable ist.
        # Flask braucht etwas in Json, bzw. etwas was in Json umgewandelt werden kann

# ========================================
# ================USERS---================
# ========================================
# Resource, weil Flaskrestful ein Objekt auf eine Route binden muss. Dieses Objekt
# beinhlatet die HTTP-Methoden, die auf dieser Resource verwendet werden können und diese in dieser Klasse implementiert.
class UseResourceUsers(Resource):

    # Die Methoden MÜSSEN GET POST DELETE UND PUT heißen !!!
    # POST = ADD
    #@auth.login_required
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

    @auth.login_required
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

    #@auth.login_required
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

    #@auth.login_required
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
# ================USERS---================
# ========================================
class UseResourceUsersUI(Resource):

    @auth.login_required
    def get(self, id):
        user = User.query.get(id)
        rto = []

        rto.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password
        })

        return rto

    # @auth.login_required
    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return 200

    def put(self, id):
        user = User.query.get(id)
        parser = reqparse.RequestParser()
        username = parser.parse_args().username
        email = parser.parse_args().email
        password = parser.parse_args().password

        user.username = username
        user.email = email
        user.password = password

        db.session.commit()
        return 200





# ========================================
# ================Messages================
# ========================================
class UseResourceMessages(Resource):
    @auth.login_required
    def post(self):
        # Übersetzer: von Request zu Python übersetzt
        parser = reqparse.RequestParser()
        # Die Argumente username und email müssen vorhanden sein
        parser.add_argument('text', type=str)
        #ID des aktuell-eingeloggten Users wird verwendet.
        id = User.query.filter_by(username=auth.username()).first().id
        #parser.add_argument('owner', type=int)
        # Fügt das Objekt in die Datenbank hinzu
        db.session.add(Message(text=parser.parse_args().text,owner=id))
        db.session.commit()
        # Returned etwas
        return 'success', 200

    #@auth.login_required
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

    #@auth.login_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("messageID", type=int)
        id = parser.parse_args().messageID
        message = Message.query.get(id)
        db.session.delete(message)
        db.session.commit()
        return "successfully deleted", 200

    #@auth.login_required
    def put(self):
        # Übersetzer: von Request zu Python übersetzt
        parser = reqparse.RequestParser()
        # ID muss vorhanden sein bei dem Request
        parser.add_argument('messageID', type=int)
        parser.add_argument('text', type=str)
        parser.add_argument('owner', type=int)
        # Übersetzt HTTP-Argumente in Python-Variable
        id = parser.parse_args().messageID

        # Der User, welcher geändert werden soll wird durch die id definiert
        message = Message.query.get(id)
        # username soll geändert werden
        text = parser.parse_args().text
        # email soll geändert werden
        owner = parser.parse_args().owner

        # derzeitiger username und derzeitige email wird ersetzt
        message.text = text
        message.owner = owner

        db.session.commit()
        return 'successfully updated', 200

# ========================================
# ================Message================
# ========================================
class UseResourceMessagesUI(Resource):

    #@auth.login_required
    def get(self, messageID):
        message = Message.query.get(messageID)
        rto=[]

        rto.append({
            'messageID': message.messageID,
            'text': message.text,
            'owner': message.owner
        })

        return rto

    #@auth.login_required
    def delete(self, messageID):
        message = Message.query.get(messageID)
        db.session.delete(message)
        db.session.commit()
        return 200




# Hier wird der Pfad erstellt, wo diese Resource zur Verfügung gestellt wird.
api.add_resource(UseResourceUsers, '/users')
api.add_resource(UseResourceUsersUI, '/users/<id>')
api.add_resource(UseResourceMessages, '/chat')
api.add_resource(UseResourceMessagesUI, '/chat/<messageID>')
api.add_resource(Login, '/login')
# Wenn main-Thread ausgeführt wird die Flask-App mit Werkzeug ausgeführt. Werkzeug ist nicht für ein öffentliches Deployment empfohlen.
if __name__ == '__main__':
    app.run(debug=True)