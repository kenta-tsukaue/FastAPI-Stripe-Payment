from fastapi import FastAPI, Body, Depends, Path, HTTPException, Response, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import models
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
import handle_db
import uuid
import stripe

stripe.api_key = "YOUR_PUBLIC_KEY"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(path="/")
async def FastAPI():
    return { "message" : "Hello World" }

@app.get(path="/auth")
async def post_user(token = Cookie(None)):
    print(token)
    result = handle_db.search_token(token)
    return result


## create user
@app.post(path="/signup")
async def post_user(body=Body(...)):
    print(body)
    result = handle_db.create_user(body["name"], body["email"], body["password"])
    if result == 1:
        raise HTTPException(status_code=404, detail="Query Error!!")
    return result

## select user
@app.post(path="/login")
async def get_user(response: Response, body = Body(...)):
    print(body)
    result = handle_db.login_user(body["email"], body["password"])
    if result == 1:
        raise HTTPException(status_code=404, detail="Query Error!!")
    if result["isLoggedIn"]:
        token=str(uuid.uuid4())
        handle_db.add_token(result["id"], token)
        response.set_cookie(key="token", value=token, httponly=True)
    return result

@app.get(path="/logout")
async def logout_user(response: Response):
    response.delete_cookie("token")
    return "complete logout"

@app.post(path="/pay")
async def pay(body = Body(...)):
    email = body["email"]
    amount = body["amount"]
    print(email, amount)
    if not email:
        return 'You need to send an Email!'

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency='JPY',
        receipt_email=email
    )

    return {"client_secret": intent['client_secret']}

@app.get(path="/getUsers")
async def getUsers():
    print(handle_db.get_userInfo())
    return(handle_db.get_userInfo())