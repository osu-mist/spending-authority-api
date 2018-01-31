from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class OnidForm(FlaskForm):
    onid = StringField('ONID', validators=[DataRequired()])
    submit = SubmitField('Submit')
