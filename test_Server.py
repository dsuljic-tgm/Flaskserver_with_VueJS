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

def test_ping(client):
    # Methoden können durch test_client() aufgerufen und getestet werden
    assert client.get('/').status_code == 200

def test_post(client):
    answ = client.post("/", data={
        "username":"Richard",
        "email":"rwutscher@gmail.com",
        "password":"password"
    })
    
    assert answ.status_code == 200

    answ2 = client.get("/")
    assert answ2.json == [{"id": 1, "username":"Richard", "email":"rwutscher@gmail.com", "password":"password"}]

def test_delete(client):
    client.post("/", data={
        "username":"Richard",
        "email":"rwutscher@gmail.com",
        "password": "password"
    })

    client.post("/", data={
        "username":"Richard2",
        "email":"rwutscher2@gmail.com",
        "password": "password"
    })

    client.delete("/", data={"id":2})
    answ = client.get("/")
    assert answ.json == [{"id": 1, "username": "Richard", "email": "rwutscher@gmail.com","password":"password"}]

def test_update(client):
    client.post("/", data={
        "username": "Richard",
        "email": "rwutscher@gmail.com",
        "password": "password"
    })

    client.put("/", data={
        "id": 1,
        "username": "Dzenan",
        "email": "dsuljic@gmail.com",
        "password": "password"
    })

    answ = client.get("/")
    assert answ.json == [{"id": 1, "username": "Dzenan", "email": "dsuljic@gmail.com", "password": "password"}]