"""
castLabs JWT "proxy" implementation using fastapi 

Basic requirements:
- appends JWT token in x-my-jwt header
- docker and docker-compose infrastructure
- Makefile

Bonus points:
- async
- provides /status with time since startup in secs and number of processed requests

TODO:
- tests
"""

from fastapi import FastAPI, Request, Response
from datetime import datetime, timedelta
import os
import httpx
from uuid import uuid4
import jwt

app = FastAPI()

START_TIME = datetime.now()
REQUESTS = 0
JWT_SECRET = os.getenv(
    "JWT_SECRET",
    "a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf",
)
POST_URL = os.getenv("POST_URL", "https://postman-echo.com/post")


@app.get("/status")
async def status():
    current_time = datetime.now()
    since_start = current_time - START_TIME
    return {"uptime": since_start.total_seconds(), "no_requests": REQUESTS}


@app.post("/")
async def root(request: Request):
    global REQUESTS
    REQUESTS += 1

    data = {
        "iat": datetime.utcnow(),
        "jti": str(uuid4().hex),
        "user": "username",
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
    }

    j = jwt.encode(data, JWT_SECRET, algorithm="HS512")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            POST_URL,
            data=await request.json(),
            headers={"x-my-jwt": j, "content-type": request.headers["content-type"]},
        )

    return Response(status_code=resp.status_code, content=resp.content, headers=resp.headers)
