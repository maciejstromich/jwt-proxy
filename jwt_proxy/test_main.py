import json

import jwt

from fastapi.testclient import TestClient

from .main import app, JWT_SECRET


def test_post_main():
    """
    Simple test case checking if the required keys are inside the x-my-jwt header
    To further improve testing:
    - mock post to postman-echo.com
    - mock methods used to generate the date, jti, date
    - assert correct values are returned in the x-my-jwt
    """
    client = TestClient(app)
    data = {"key": "value"}
    response = client.post("/", headers={"content-type": "application/json"}, json=data)
    assert response.status_code == 200

    j = response.json()
    assert j["data"] == "key=value"
    assert "x-my-jwt" in j["headers"].keys()

    my_jwt = jwt.decode(j["headers"]["x-my-jwt"], JWT_SECRET, algorithms=["HS512"])
    assert "date" in my_jwt.keys()
    assert "iat" in my_jwt.keys()
    assert "jti" in my_jwt.keys()
    assert "user" in my_jwt.keys()
