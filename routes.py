from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Message
from app import app, db, mail
from models import Room, Amenity, BookingInquiry, ContactInquiry
from forms import BookingForm, ContactForm
from datetime import datetime, date

@app.route('/')
def index():
    """Home page with featured rooms and amenities"""
    featured_rooms = Room.query.filter_by(is_available=True).limit(3).all()
    featured_amenities = Amenity.query.filter_by(is_active=True).limit(4).all()
    return render_template('index.html', rooms=featured_rooms, amenities=featured_amenities)

@app.route('/rooms')
def rooms():
    """Rooms and suites page"""
    all_rooms = Room.query.filter_by(is_available=True).all()
    return render_template('rooms.html', rooms=all_rooms)

@app.route('/amenities')
def amenities():
    """Hotel amenities page"""
    all_amenities = Amenity.query.filter_by(is_active=True).all()
    
    # Group amenities by category
    amenities_by_category = {}
    for amenity in all_amenities:
        if amenity.category not in amenities_by_category:
            amenities_by_category[amenity.category] = []
        amenities_by_category[amenity.category].append(amenity)
    
    return render_template('amenities.html', amenities_by_category=amenities_by_category)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    """Booking inquiry page"""
    form = BookingForm()
    rooms = Room.query.filter_by(is_available=True).all()
    
    # Populate room choices
    form.room_id.choices = [(room.id, f"{room.name} - ${room.price_per_night}/night") for room in rooms]
    
    if form.validate_on_submit():
        try:
            # Create booking inquiry
            inquiry = BookingInquiry()
            inquiry.guest_name = form.guest_name.data
            inquiry.email = form.email.data
            inquiry.phone = form.phone.data
            inquiry.room_id = form.room_id.data
            inquiry.check_in = form.check_in.data
            inquiry.check_out = form.check_out.data
            inquiry.adults = form.adults.data
            inquiry.children = form.children.data
            inquiry.special_requests = form.special_requests.data
            
            db.session.add(inquiry)
            db.session.commit()
            
            # Send confirmation email if mail is configured
            try:
                if app.config['MAIL_USERNAME']:
                    room = Room.query.get(form.room_id.data)
                    msg = Message(
                        'Booking Inquiry Confirmation - The Oasis Hotel & Spa',
                        recipients=[str(form.email.data)]
                    )
                    if room:
                        msg.body = f"""
Dear {form.guest_name.data},

Thank you for your booking inquiry at The Oasis Hotel & Spa.

Booking Details:
- Room: {room.name}
- Check-in: {form.check_in.data}
- Check-out: {form.check_out.data}
- Guests: {form.adults.data} adults, {form.children.data} children
- Special Requests: {form.special_requests.data or 'None'}

We will contact you within 24 hours to confirm your booking.

Best regards,
The Oasis Hotel & Spa Team
                        """
                    mail.send(msg)
            except Exception as e:
                app.logger.error(f"Failed to send email: {e}")
            
            flash('Your booking inquiry has been submitted successfully! We will contact you soon.', 'success')
            return redirect(url_for('booking'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Booking error: {e}")
            flash('An error occurred while processing your booking. Please try again.', 'error')
    
    return render_template('booking.html', form=form, rooms=rooms)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            # Create contact inquiry
            inquiry = ContactInquiry()
            inquiry.name = form.name.data
            inquiry.email = form.email.data
            inquiry.subject = form.subject.data
            inquiry.message = form.message.data
            
            db.session.add(inquiry)
            db.session.commit()
            
            # Send acknowledgment email if mail is configured
            try:
                if app.config['MAIL_USERNAME']:
                    msg = Message(
                        'Contact Inquiry Received - The Oasis Hotel & Spa',
                        recipients=[str(form.email.data)]
                    )
                    msg.body = f"""
Dear {form.name.data},

Thank you for contacting The Oasis Hotel & Spa.

Your inquiry has been received and we will respond within 24 hours.

Subject: {form.subject.data}
Message: {form.message.data}

Best regards,
The Oasis Hotel & Spa Team
                    """
                    mail.send(msg)
            except Exception as e:
                app.logger.error(f"Failed to send email: {e}")
            
            flash('Your message has been sent successfully! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Contact error: {e}")
            flash('An error occurred while sending your message. Please try again.', 'error')
    
    return render_template('contact.html', form=form)

@app.route('/gallery')
def gallery():
    """Hotel gallery page"""
    return render_template('gallery.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
