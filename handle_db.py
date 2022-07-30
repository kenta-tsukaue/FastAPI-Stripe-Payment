
# -*- encoding: utf-8 -*-
import sys

from sqlalchemy.sql.expression import false
from passlib.context import CryptContext
import models
import databases

sys.dont_write_bytecode = True

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(user_name, user_mail, user_password):
    session = databases.create_new_session()
    pre_user = session.query(models.user).\
                filter(models.user.email == user_mail).\
                first()
    print(pre_user)
    if pre_user == None:
        hash = get_password_hash(user_password)
        user = models.user()
        user.name = user_name
        user.email = user_mail
        user.password = hash
        session.add(user)
        #ちなみにsession.delete(userで削除)
        session.commit()
        return {"result":True}
    else :
        return {"result":False}

def login_user(user_mail, user_password):
    session = databases.create_new_session()

    user = session.query(models.user).\
                filter(models.user.email == user_mail).\
                first()
    if user == None:
        result = {"isLoggedIn":False}
    else :
        if verify_password(user_password, user.password):
            result = {"isLoggedIn":True, "id":user.id }
        else :
            result = {"isLoggedIn":False}
    return result

def add_token(user_id, token):
    session = databases.create_new_session()
    user = session.query(models.user).\
                filter(models.user.id == user_id).\
                first()
    user.token = token
    session.commit()


def search_token(token):
    if token == None:
        return {"auth":False}
    session = databases.create_new_session()
    user = session.query(models.user).\
                filter(models.user.token == token).\
                first()
    if user == None:
        result = {"auth":False}
    else :
        result = {"auth":True, "id":user.id}
    return result

def get_userInfo():
    session = databases.create_new_session()
    user_id = session.query(models.user.id, models.user.email).all()
    return user_id