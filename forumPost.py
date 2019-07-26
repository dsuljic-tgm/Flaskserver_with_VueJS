from app import Forumpost, User, auth, db
from flask_restful import Resource, reqparse

# ========================================
# ================ForumPost===============
# ========================================
class UseResourceForumPosts(Resource):
    @auth.login_required
    def post(self):
        # Übersetzer: von Request zu Python übersetzt
        parser = reqparse.RequestParser()
        # Die Argumente username und email müssen vorhanden sein
        parser.add_argument('title', type=str)
        parser.add_argument('text', type=str)
        #ID des aktuell-eingeloggten Users wird verwendet.
        #parser.add_argument('owner', type=int)
        # Fügt das Objekt in die Datenbank hinzu
        db.session.add(Forumpost(title=parser.parse_args().title, text=parser.parse_args().text))
        db.session.commit()
        # Returned etwas
        return 'success', 200

    #@auth.login_required
    def get(self):
        # rto = return Object, json array
        rto = []
        # iterriert durch alle Userobjekte, weil User.query.all() nicht JSON-Serializable ist.
        # Flask braucht etwas in Json, bzw. etwas was in Json umgewandelt werden kann
        for element in Forumpost.query.all():
            # fügt alle Atribute vom User in ein neues Objekt, welches in das returnobjectliste hinzugefügt wird.
            rto.append({
                "postID": element.postID,
                "title": element.title,
                "text": element.text,
            })
        return rto

    #@auth.login_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("postID", type=int)
        id = parser.parse_args().postID
        forumpost = Forumpost.query.get(id)
        db.session.delete(forumpost)
        db.session.commit()
        return "successfully deleted", 200

    #@auth.login_required
    def put(self):
        # Übersetzer: von Request zu Python übersetzt
        parser = reqparse.RequestParser()
        # ID muss vorhanden sein bei dem Request
        parser.add_argument('postID', type=int)
        parser.add_argument('title', type=str)
        parser.add_argument('text', type=str)
        # Übersetzt HTTP-Argumente in Python-Variable
        id = parser.parse_args().postID

        # Der User, welcher geändert werden soll wird durch die id definiert
        forumpost = Forumpost.query.get(id)
        # username soll geändert werden
        title = parser.parse_args().title
        text = parser.parse_args().text
        # email soll geändert werden

        # derzeitiger username und derzeitige email wird ersetzt
        forumpost.title = title
        forumpost.text = text

        db.session.commit()
        return 'successfully updated', 200

# ========================================
# ================ForumPost===============
# ========================================
class UseResourceForumPostsUI(Resource):

    #@auth.login_required
    def get(self, postID):
        forumpost = Forumpost.query.get(postID)
        rto=[]

        rto.append({
            'postID': forumpost.postID,
            'title': forumpost.title,
            'text': forumpost.text
        })

        return rto

    #@auth.login_required
    def delete(self, postID):
        forumpost = Forumpost.query.get(postID)
        db.session.delete(forumpost)
        db.session.commit()
        return 200

    def put(self, postID):
        forumpost = Forumpost.query.get(postID)

        parser = reqparse.RequestParser()

        parser.add_argument('title', type=str)
        parser.add_argument('text', type=str)

        title = parser.parse_args().title
        text = parser.parse_args().text

        forumpost.title=title
        forumpost.text = text

        db.session.commit()
        return 200
