from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, URL
from flask_wtf import FlaskForm

class UserForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    box_number = IntegerField('N.ro Box', validators=[DataRequired()])
    submit = SubmitField('Submit')