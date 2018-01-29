from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from gboard import db
from gboard.infrastructure import Domain, Server
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms_alchemy import ModelFieldList
from wtforms.fields import FormField

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class ServerForm(ModelForm):
    class Meta:
        model = Server

class DomainForm(ModelForm):
    class Meta:
        model = Domain
    master = QuerySelectField(label='Master', allow_blank=False)
    servers = ModelFieldList(FormField(ServerForm))


class DomainSelectForm(FlaskForm):
    left_domain = QuerySelectField(label='Domain', allow_blank=False)
    right_domain = QuerySelectField(label='Domain', allow_blank=False)