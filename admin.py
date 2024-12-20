from fastapi import FastAPI
from sqladmin import Admin, ModelView

from core.db import sqlalchemy_config as config
from bot.models import UserModel


app = FastAPI()
engine = config.get_engine

admin = Admin(app, engine)


class UserAdmin(ModelView, model=UserModel):
    column_list = '__all__'


admin.add_view(UserAdmin)
