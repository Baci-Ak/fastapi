from fastapi.testclient import TestClient
import pytest
from app.main import app
# from app import schemas, models
from app.database import get_db, Base
from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app import schemas, models
from app.oauth2 import create_access_token
#import psycopg


#SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)





#client = TestClient(app)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# tests/database.py
@pytest.fixture
def test_user(client):
    user_data = {"email": "paul2@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = schemas.UserOut(**res.json())
    return {**user_data,"id": new_user.id}

@pytest.fixture
def test_user2(client):
    user_data = {"email": "paul1@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = schemas.UserOut(**res.json())
    return {**user_data,"id": new_user.id}


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers,"Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {"title": "first title", "content": "first content", "user_id": test_user["id"]},
        {"title": "2nd title", "content": "2nd content", "user_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "user_id": test_user["id"]},
        {"title": "4th title", "content": "4th content", "user_id": test_user["id"]},
        {"title": "5th title", "content": "5th content", "user_id": test_user["id"]},
        {"title": "6th title", "content": "6th content", "user_id": test_user2["id"]},
        
    ]
    def create_post(post):
        return models.Post(**post)
    post_map = map(create_post, posts_data)
    post_list = list(post_map)
    session.add_all(post_list)
    session.commit()
    posts = session.query(models.Post).all()
    return posts