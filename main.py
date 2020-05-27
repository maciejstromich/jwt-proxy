"""
This is not a true proxy which can be used as --proxy parameter in curl.

It's just implementation of requirements for castLabs python programming task using FastAPI framework. 
Implementation takes the most common approach of solving the programming task.

Implementation time: 1h
"""

from fastapi import FastAPI, Request, Response
from datetime import datetime, timedelta
import os
import httpx
from uuid import uuid4
import jwt 

START_TIME = datetime.now()
REQUESTS = 0
JWT_SECRET = os.getenv("JWT_SECRET", "a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf")
POST_URL = os.getenv("POST_URL", "https://postman-echo.com/post")
app = FastAPI()


@app.get("/status")
async def status():
    current_time = datetime.now()
    since_start = current_time - START_TIME
    return {
        "uptime": since_start.total_seconds(),
        "no_requests": REQUESTS
     }


@app.post("/*")
async def root(request: Request):
    global REQUESTS 
    REQUESTS += 1
    data = {
        "iat": datetime.utcnow(),
        "jti": str(uuid4().hex)
    }
    
    j =  jwt.encode(data, JWT_SECRET, algorithm="HS512")

    async with httpx.AsyncClient() as client:
        resp = await client.post(POST_URL, data=await request.json(), headers={"x-my-jwt": j})
    
    return Response(status_code=resp.status_code, content=resp.content)



