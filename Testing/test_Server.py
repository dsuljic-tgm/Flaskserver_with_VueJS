import pytest
import flask
from app import app, db

# Before Each
@pytest.fixture
def client():
    # erstellt die Datenbank zu Beginn des Tests
    db.create_all()

    # Alles was nach dem yield passiert wird auch noch ausgeführt
    yield app.test_client()

    # löscht die Datenbank nach dem Test
    db.drop_all()

def test_ping_User(client):
    # Methoden können durch test_client() aufgerufen und getestet werden
    assert client.get('/users').status_code == 200

def test_post_User(client):
    answ = client.post("/users", data={
        "username":"Richard",
        "email":"rwutscher@gmail.com",
        "password":"password"
    })
    
    assert answ.status_code == 200

    answ2 = client.get("/users")
    assert answ2.json == [{"id": 1, "username":"Richard", "email":"rwutscher@gmail.com", "password":"password"}]

def test_delete_User(client):
    client.post("/users", data={
        "username":"Richard",
        "email":"rwutscher@gmail.com",
        "password": "password"
    })

    client.post("/users", data={
        "username":"Richard2",
        "email":"rwutscher2@gmail.com",
        "password": "password"
    })

    client.delete("/users", data={"id":2})
    answ = client.get("/users")
    assert answ.json == [{"id": 1, "username": "Richard", "email": "rwutscher@gmail.com","password":"password"}]

def test_update_User(client):
    client.post("/users", data={
        "username": "Richard",
        "email": "rwutscher@gmail.com",
        "password": "password"
    })

    client.put("/users", data={
        "id": 1,
        "username": "Dzenan",
        "email": "dsuljic@gmail.com",
        "password": "password"
    })

    answ = client.get("/users")
    assert answ.json == [{"id": 1, "username": "Dzenan", "email": "dsuljic@gmail.com", "password": "password"}]


def test_get_Message(client):
    answ1 = client.post("/users", data={
        "username": "Richard",
        "email": "rwutscher@gmail.com",
        "password": "password"
    })
    assert answ1.status_code == 200

    answ2 = client.post("/posts", data={"title": "Forumpost1", "text": "Ich bin der erste Forumpost"})
    assert answ2.status_code == 200

    answ3 = client.post("/chat", data={"text": "Find ich toll", "owner": 1, "forumPost": 1})
    assert answ3.status_code == 200

    answ4 = client.get("/chat")

    #assert answ4.json == [{"messageID": 1, "text": "Find ich toll", "owner": 1, "forumPost": 1}]
