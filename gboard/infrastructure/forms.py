from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from gboard import db
from gboard.infrastructure import Domain, Server

from wtforms_alchemy import ModelFieldList
from wtforms.fields import FormField

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class DomainForm(ModelForm):
    class Meta:
        model = Domain

    server = ModelFieldList(FormField(ServerForm))

class ServerForm(ModelForm):
    class Meta:
        model = Server
    
    domains = ModelFieldList(FormField(DomainForm))