from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

data = {
    "email": "abc@mail.ru",
    "bio": "I'm happy",
    "age": 12,
}

data_wo_age = {
    "email": "abc@mail.ru",
    "bio": "I'm happy",
}


class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=1000)


users = []


@app.post("/users")
def add_user(user: UserSchema):
    users.append(user)
    return {"ok": True, "msg": "User added"}


@app.get("/")
def root():
    return {"ok": True, "hint": "Открой /docs или используй /users (GET/POST)"}


@app.get("/users")
def get_users():
    return users


class UserAgeSchema(UserSchema):
    age: int | None = Field(default=None, ge=0, le=130)


# print(repr(UserSchema(**data)))
# print(repr(UserAgeSchema(**data_wo_age)))


# # les_2/main.py с app внутри, как запустить только этот код
# uvicorn les_2.main:app --reload
