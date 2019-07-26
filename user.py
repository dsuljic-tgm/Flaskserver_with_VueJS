from app import User, auth, db
from flask_restful import Resource, reqparse

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

        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

        username = parser.parse_args().username
        email = parser.parse_args().email
        password = parser.parse_args().password

        user.username = username
        user.email = email
        user.password = password

        db.session.commit()
        return 200

