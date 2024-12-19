from fastapi import FastAPI
from sqladmin import Admin, ModelView

# from app import app
from db import engine
from models import UserModel

app = FastAPI()
admin = Admin(app, engine)


class UserAdmin(ModelView, model=UserModel):
    column_list = "__all__"


admin.add_view(UserAdmin)
