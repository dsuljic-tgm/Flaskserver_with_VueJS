from app import User, auth, db
from flask_restful import Resource, reqparse

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
            # returned die UserID des Users, immer 200 returnen
            return user.id
        else:
            return 'Wrong password, please try again', 402

        # iterriert durch alle Userobjekte, weil User.query.all() nicht JSON-Serializable ist.
        # Flask braucht etwas in Json, bzw. etwas was in Json umgewandelt werden kann
