from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DecimalField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange
from wtforms import HiddenField

# ------------------ AUTENTICACIÓN ------------------

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    
    # Agregado el campo de rol para evitar el error en la plantilla
    role = SelectField('Role', choices=[('Student', 'Student'), ('Professor', 'Professor')], validators=[DataRequired()])
    
    submit = SubmitField('Register')

# ------------------ CAMBIO DE CONTRASEÑA ------------------

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password', message="Passwords must match.")])
    submit = SubmitField('Change Password')


# ------------------ FORMULARIO ITEM ------------------

class ItemForm(FlaskForm):
    id = HiddenField()
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    categoria = StringField('Categoría', validators=[DataRequired(), Length(max=50)])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    precio_estimado = DecimalField('Precio Estimado', places=2, validators=[DataRequired()])
    ubicacion = StringField('Ubicación', validators=[DataRequired(), Length(max=100)])
    fecha_adquisicion = DateField('Fecha de Adquisición', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Guardar')
