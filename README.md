
# Restful-Forum
  
  
## Implementierung  
### Einleitung  
Das Ziel der Übung war das Verständnis von zustandslosen Verbindungen um Daten leicht administrieren und verteilen zu können. Für diese Aufgabe habe ich folgende Sachen verwendet:  
  
 - Python
 - GitHub
 - Flask
 - Pytest
 - Tox
 - Travis-CI
 - Vue
 - Cypress
 - HTTP Basic Auth
  
  
### Flask  
Flask ist ein Microframework, da es keine speziellen Werkzeuge, beziehungsweise Bibliotheken erfordert. Es verfügt über keine Formularüberprüfungen oder andere Komponenten, bei denen bereits vorhandene Bibliotheken benötigt werden. Flask wird mittels der Requirements.txt importiert.  
  
### Pytest  
  
Pytest hilft uns einfache Tests zu schreiben. In unserem Fall testen wir die HTTP-Methoden, welche wir in unserem Server zusammmengeschrieben habe. Mit Pytest kann ich nun beispielsweise testen, ob ein User erstellt wird.  
  
## Server (app.py)  
  
### Einleitung  
Der Server den wir in dieser Übung verwenden, ist eine einfache REST-API, welche mit Python und Flask gebaut wird. Im Server, welcher bei uns "*app.py*" heißt, werden neue Datensätze erstellt, abgerufen,  aktualisiert und gelöscht. Daher können wir sagen, dass unser Server die CRUD-Befehle ausführen (Create, Read, Update, Delete). Standartgemäß läuft der Server auf  *http://127.0.0.1:5000/*.  
  
### Anwendung  
In unserem Beispiel werden User erstellt, welche folgende Attribute haben:  
  
#### User:    
|Attribut| Wert |Beziehung |  
|--|--|--|  
| ID | Integer | Primary-Key  
| Username | String | Unique  
| Email | String | Unique  
| Password | String | Multiple  
  
#### Message:     
|Attribut| Wert |Beziehung |  
|--|--|--|  
| ID | Integer | Primary-Key  
| text | String | Unique  
| owner | String | Unique  
| forumpost | ForeignKey | Multiple    

#### Forumpost:    
|Attribut| Wert |Beziehung |  
|--|--|--|  
| ID | Integer | Primary-Key  
| title | String | Unique  
| text | String | Unique  


Nun können wir beispielsweise einen Benutzer erstellen, anzeigen lassen, aktualisieren oder auch löschen. Dies bietet uns die Möglichkeit, den User und alle anderen Objekte zu testen und verschiedene Szenarien auszuführen, sodass der Server auch keine Inkonsistenz aufweist.  
  
  
### Unittests  
Mit den Unittests wurden die CRUD-Befehle direkt am Server getestet. Hier wurde beispielsweise geschaut, ob der User richtig angezeigt wird. Außerdem wurde beachtet das mehrere User sich nicht überschreiben können, sodass es zu einer konsistenten Datenbank bleibt. Dies wurde mit der Anzahl der Benutzer überprüft.  
  
Insgesamt gibt es zurzeit 10 Unittests, welche die CRUD-Befehle überprüfen. Um die Unittests auszuführen, muss der server gestartet werden (siehe Anleitung)  
  
## Simple Forum (VUE)  
  
### VUE  
Vue.js ist ein clientseitiges JavaScript-Webframework, welches uns beim erstellen der Single-Page-GUI, für das verwalten der Benutzer und den anderen Objekten helfen wird. Die GUI kann mittels *http://localhost:8080/#/users* aufgerufen werden. Hier werden alle User, welche wir erstellt haben angezeigt. Diese können wir mit der benutzeroberfläche löschen, aktualisieren und hinzufügen. Alle Benutzer werden in einer Tabelle gelistet, sodass es übersichtlich bleibt.  
  
**Der Server muss vorher gestartet werden (siehe Anleitung).**  
  
### Anleitung  
  
 1. *app.py* starten
 2. Nachdem erfolgreichen starten des Servers die CMD öffnen  
 3. Zum folgenden Verzeichnis wechseln: *(\src\main\vue\client)*  
 4. `npm run dev` ausführen (zuvor sollte Npm installiert sein)  
 5. Die Website ist nun erreichbar (*http://localhost:8080/#/users*)  
   
 Standartgemäß befindet sich der Port des Servers auf **5000**, und der Port des Clients auf **8080**. Dies kann nur im Code geändert werden, und nicht in einer GUI selber!  
  
  
### Cypress  
Mit Cypress kann man eigentlich alles testen, was auf dem Browser läuft. Daher bietet es sich an, unseren Client, welcher auf der Website angezeigt wird mit Cypress zu testen. Genauso wie bei den Unittests wurden die CRUD-Befehle und verschiedene Szenarien getestet.  
  
Insgesamt gibt es zurzeit 6 Files, wobei insgesamt 21 Commands ausgeführt werden. Auch hier muss der Server gestartet werden und auch der Client (siehe Anleitung).  
  
**Um Cypress zu starten muss man folgendendes in die CMD eingeben:** `npx cypress open` im Verzeichnis *\src\main\vue\client*  
  
Nun öffnet sich ein Fenster, in welchem wir aussuchen können, welche Tests ausgeführt werden sollen.  
  
### Travic-CI  
Mit Travis-CI ist es uns möglich Projekte zu testen. Diese Tests werden gesammelt, sodass alles zusammen in Travis getestet wird.  
  
Folgende Schritte muss man ausführen, bevor man mit Travis startet  
  
 - Einloggen mit GitHub  
 - Email bestätigen  
 - Travis CI auf der Website aktivieren  
 - Eine .travis.yml in das Projekt einfügen  
  
In das .travis.yml File, kommen dann Informationen, wie beispielsweise Programmiersprache, Requirements, Directories, etc. hinein. Da wir auch mit Tox arbeiten, können wir die Tests alle aufeinmal in Travis ausführen, sodass wir einen Überblick auf die bisherigen Erfolge und Misserfolge des Projektes haben.  
  
Es ist wichtig zu beachten, dass man die modules, welche man benötigt auch überall hinzufügt, sonst kann es sein, dass Travis Fehler ausgibt, welche schwer zu lesen sind.  
  

## Authentifizierung mit HTTP Basic Auth
HTTP Baisc Auth reicht für sehr einfache Anwendungen aus. Mit Flask haben wir die Möglichkeit dies sehr einfach zu implementieren. Durch die einfache Authentifizierung ist es uns möglich bestimmte Funktionen nur für angemeldete Nutzer freizugeben. Damit wir einen Benutzer haben, welcher Zugriff auf die Funktionen hat, müssen wir einen in der Main-Methode erstellen:

    if __name__ == '__main__':  
    db.create_all()  
    db.session.add(User("Dzenan", "test", "dsuljic@student.tgm.ac.at", "photo123"))  
    db.session.commit()  
    app.run(debug=True)
  Um den Server auszuführen müssen wir server.py starten (\src\main\python\server\server.py). Nachdem wir uns angemeldet haben können wir uns mit diesem User alle CRUD-Befehel ausführen, mittel CURL oder Insomnia.


## Lessons Learned  
  
 - Überprüfen, ob der Server die Datenbank neu lädt.  
 - Überprüfen, ob der Server eingeschaltet ist.  
 - Commands immer im richtigen Verzeichnis ausführen.  
 - Für Cypress mit Travis, sollte die package.json immer aktualisiert sein.  
 - Komplizierte Module-Fehler in Travis können mit einem einfachen npm install gelöst werden.  
 - Nach jeder Änderung commiten, da auch Kommentare Fehler verursachen können.  
 - Einzelne Tests sollen immer ausführbar sein (vor dem Test User erstellen beispielsweise).  
 - Immer den richtigen Port ansprechen.  
  
  
## Quellen  
  
 - https://github.com  
 - http://flask.pocoo.org/  
 - https://docs.pytest.org/en/latest/  
 - https://pypi.org/project/tox/  
 - https://travis-ci.com/  
 - https://pytest-qt.readthedocs.io/en/latest/reference.html  
 - https://www.cypress.io/  
 - https://docs.python.org/3/  
 - https://vuejs.org/  
 - https://www.npmjs.com/
 - http://flask.pocoo.org/snippets/8/
 - https://www.digitalocean.com/

