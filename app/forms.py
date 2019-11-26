from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from wtforms.fields.html5 import DateField
from app.models import User



class LoginForm (FlaskForm):
    username = StringField( 'Username', validators=[DataRequired()] )
    password = PasswordField( 'Password', validators=[DataRequired()] )
    remember_me = BooleanField( 'Remember Me')
    submit = SubmitField( 'Sign In')


class RegistrationForm (FlaskForm):
    username = StringField( 'Username', validators=[DataRequired()] )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField( 'Password', validators=[DataRequired()] )
    password2 = PasswordField('Repeate Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')


class IndexForm(FlaskForm):
    date = DateField('date', format='%Y-%m-%d')
    submitDate = SubmitField('OK')


class CheckForm(FlaskForm):
    check = BooleanField()
    submitCheck = SubmitField('Add to observed')
