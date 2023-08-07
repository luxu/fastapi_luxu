from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.models import User
from fast_zero.database import get_session
from fast_zero.schemas import UserSchema, UserPublic, UserDB, UserList, Message

app = FastAPI()

database = []

@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}

@app.post('/users/', response_model=UserPublic, status_code=201)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )

    db_user = User(
        username=user.username,
        password=user.password,
        email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id

@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    del database[user_id - 1]

    return {'detail': 'User deleted'}
