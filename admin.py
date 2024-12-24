from fastapi import FastAPI
from sqladmin import Admin, ModelView

from core.config import sqlalchemy_config as config
from core.models import UserModel, ServiceModel


app = FastAPI()
engine = config.get_engine

admin = Admin(app, engine)


class UserAdmin(ModelView, model=UserModel):
    column_list = '__all__'


class ServiceAdmin(ModelView, model=ServiceModel):
    column_list = '__all__'


admin.add_view(UserAdmin)
admin.add_view(ServiceAdmin)
