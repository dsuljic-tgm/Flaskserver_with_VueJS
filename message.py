from app import Message, User, auth, db
from flask_restful import Resource, reqparse

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
        # Fügt das Objekt in die Datenbank hinzu
        db.session.add(Message(text=parser.parse_args().text,owner=id, forumPost=parser.parse_args().forumPost))
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
                "owner": element.owner,
                "forumPost": element.forumPost
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

        # derzeitiger username und derzeitige email wird ersetzt
        message.text = text

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
            'owner': message.owner,
            'forumPost':message.forumPost
        })

        return rto

    #@auth.login_required
    def delete(self, messageID):
        message = Message.query.get(messageID)
        db.session.delete(message)
        db.session.commit()
        return 200

    def put(self, messageID):
        message = User.query.get(messageID)

        parser = reqparse.RequestParser()

        parser.add_argument('text', type=str)

        text = parser.parse_args().text

        message.text = text

        db.session.commit()
        return 200
