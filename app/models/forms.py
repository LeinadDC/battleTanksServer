from wtforms import Form, BooleanField, StringField, PasswordField, validators



class RegistrationForm(Form):
    username = StringField()
    password = PasswordField()
    email = StringField()
