from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, Email

class Login(FlaskForm):
    username = StringField('Username',validators=[InputRequired(), Length(min=4,max=100)],
                           render_kw={'placeholder':'Username'})
    password = PasswordField('Password',validators=[InputRequired(), Length(min=4,max=100)],
                           render_kw={'placeholder':'Password'})
    submit = SubmitField("Login")
    
class Register(FlaskForm):
    username = StringField('Username',validators=[InputRequired(), Length(min=4,max=100)],
                           render_kw={'placeholder':'Username'})
    password = PasswordField('Password',validators=[InputRequired(), Length(min=4,max=100)],
                           render_kw={'placeholder':'Password'})
    confirm_password = PasswordField('Confirm_Password',validators=[InputRequired(),EqualTo('password')],
                           render_kw={'placeholder':'Confirm_Password'})
    submit = SubmitField("Register")
    
    
class Registrationform(FlaskForm):
    username = StringField('Username',validators=[InputRequired(),Length(min=4,max=200)],
                           render_kw={'placeholder':'Username'})
    password = PasswordField('Password',validators=[InputRequired()],
                           render_kw={'placeholder':'Password'})
    submit = SubmitField("Register")