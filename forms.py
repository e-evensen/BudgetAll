from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField
from wtforms.validators import Length, DataRequired, EqualTo, Email, InputRequired
from wtforms import ValidationError
from models import User
from database import db
from bcrypt import checkpw


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField('Username', validators=[Length(1, 10)])

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        EqualTo('confirmPassword', message='Passwords must match'),
    ])

    confirmPassword = PasswordField('Confirm Password', validators=[
        Length(min=8)
    ])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() != 0:
            raise ValidationError('Email already in use.')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message='Please enter a password.')])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect email')

    def validate_password(self, field):
        user = db.session.query(User).filter_by(email=self.email.data).first()
        if not user or not checkpw(field.data.encode('utf-8'), user.password):
            raise ValidationError('Incorrect password.')


class BalanceForm(FlaskForm):
    class Meta:
        csrf = False

    balance = DecimalField('Balance', [
        InputRequired(message='Please enter a number.')
    ])

    submit = SubmitField('Set Balance')


class IncomeForm(FlaskForm):
    class Meta:
        csrf = False

    income = DecimalField('income', [
        InputRequired(message='Please enter a number.')
    ])

    submit = SubmitField('Set Income')
