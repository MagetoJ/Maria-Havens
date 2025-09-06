from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, NumberRange, Optional, ValidationError, Length, EqualTo
from datetime import date, timedelta

class BookingForm(FlaskForm):
    guest_name = StringField('Full Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional()])
    room_id = SelectField('Room Type', coerce=int, validators=[DataRequired()])
    check_in = DateField('Check-in Date', validators=[DataRequired()], default=date.today)
    check_out = DateField('Check-out Date', validators=[DataRequired()], default=date.today() + timedelta(days=1))
    adults = IntegerField('Adults', validators=[DataRequired(), NumberRange(min=1, max=8)], default=2)
    children = IntegerField('Children', validators=[NumberRange(min=0, max=6)], default=0)
    special_requests = TextAreaField('Special Requests', validators=[Optional()])
    
    def validate_check_out(self, field):
        if field.data <= self.check_in.data:
            raise ValidationError('Check-out date must be after check-in date.')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])

class AdminLoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class AdminUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')
    ])
    is_admin = BooleanField('Admin Access')

class RoomForm(FlaskForm):
    name = StringField('Room Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price_per_night = IntegerField('Price per Night (KES)', validators=[DataRequired(), NumberRange(min=1)])
    max_occupancy = IntegerField('Max Occupancy', validators=[DataRequired(), NumberRange(min=1, max=10)])
    room_size = StringField('Room Size', validators=[Optional()])
    bed_type = StringField('Bed Type', validators=[Optional()])
    amenities = TextAreaField('Amenities (comma-separated)', validators=[Optional()])
    is_available = BooleanField('Available for Booking', default=True)
