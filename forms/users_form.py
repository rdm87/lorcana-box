from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class UserForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    box_number = IntegerField('N.ro Box', validators=[DataRequired()])
    deposit = FloatField('Anticipo', validators=[DataRequired()])
    submit = SubmitField('Submit')