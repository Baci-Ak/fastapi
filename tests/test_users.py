from app import schemas
import jwt
from app.config import settings
import pytest
    
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

def test_root(client):
    response = client.get("/")
    print(response.json().get("message"))
    assert response.json().get("message") == "bind mount works, testing"
    assert response.status_code == 200


def test_create_user(client):
    response = client.post("/users/", json={"email": "paul1@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**response.json())                                                  
    assert new_user.email == "paul1@gmail.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user["email"],"password": test_user["password"]})
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("paul@gmail.com", "password123", 403),
    ("wrongemail@gmail.com", "password123", 403),
    ("paul1@gmail.com", "wrongpassword", 403),
    ("paul1@gmail.com", None, 403)
])

def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code
    #assert response.json().get("detail") == "Invalid Credentials"
