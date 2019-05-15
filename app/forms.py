from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('contrasena', validators=[DataRequired()])
    remember_me = BooleanField('Recuerdame')
    submit = SubmitField('Ingresar')


    def validateUsername():
        pass

    def validatePsw():
        pass
