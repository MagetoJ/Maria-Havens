from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField, EmailField
from wtforms.validators import DataRequired, Email, NumberRange, Optional, ValidationError
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
