from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_mail import Message
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import app, db, mail
from models import Room, Amenity, BookingInquiry, ContactInquiry, User
from forms import BookingForm, ContactForm, AdminLoginForm, AdminUserForm, RoomForm
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
                        'Booking Inquiry Confirmation - Maria Havens',
                        recipients=[str(form.email.data)]
                    )
                    if room:
                        msg.body = f"""
Dear {form.guest_name.data},

Thank you for your booking inquiry at Maria Havens.

Booking Details:
- Room: {room.name}
- Check-in: {form.check_in.data}
- Check-out: {form.check_out.data}
- Guests: {form.adults.data} adults, {form.children.data} children
- Special Requests: {form.special_requests.data or 'None'}

We will contact you within 24 hours to confirm your booking.

Best regards,
The Maria Havens Team
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
                        'Contact Inquiry Received - Maria Havens',
                        recipients=[str(form.email.data)]
                    )
                    msg.body = f"""
Dear {form.name.data},

Thank you for contacting Maria Havens.

Your inquiry has been received and we will respond within 24 hours.

Subject: {form.subject.data}
Message: {form.message.data}

Best regards,
The Maria Havens Team
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

# ============ ADMIN ROUTES ============

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data) and user.is_admin:
            login_user(user, remember=form.remember_me.data)
            flash('Welcome to the admin dashboard!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email, password, or insufficient privileges.', 'danger')
    
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    """Admin logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/admin')
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    # Get statistics
    total_rooms = Room.query.count()
    available_rooms = Room.query.filter_by(is_available=True).count()
    total_bookings = BookingInquiry.query.count()
    pending_bookings = BookingInquiry.query.filter_by(status='pending').count()
    
    recent_bookings = BookingInquiry.query.order_by(BookingInquiry.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                         total_rooms=total_rooms,
                         available_rooms=available_rooms,
                         total_bookings=total_bookings,
                         pending_bookings=pending_bookings,
                         recent_bookings=recent_bookings)

@app.route('/admin/bookings')
@login_required
def admin_bookings():
    """Admin bookings management"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    bookings = BookingInquiry.query.order_by(BookingInquiry.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/bookings.html', bookings=bookings)

@app.route('/admin/booking/update', methods=['POST'])
@login_required
def update_booking_status():
    """Update booking status"""
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    booking_id = request.form.get('booking_id')
    new_status = request.form.get('status')
    
    if not booking_id or not new_status:
        flash('Invalid request', 'danger')
        return redirect(url_for('admin_bookings'))
    
    booking = BookingInquiry.query.get_or_404(booking_id)
    booking.status = new_status
    db.session.commit()
    
    flash(f'Booking status updated to {new_status}', 'success')
    return redirect(url_for('admin_bookings'))

@app.route('/admin/rooms')
@login_required
def admin_rooms():
    """Admin rooms management"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    rooms = Room.query.order_by(Room.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('admin/rooms.html', rooms=rooms)

@app.route('/admin/room/add', methods=['GET', 'POST'])
@login_required
def admin_add_room():
    """Add new room"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    form = RoomForm()
    if form.validate_on_submit():
        room = Room()
        room.name = form.name.data
        room.description = form.description.data
        room.price_per_night = form.price_per_night.data
        room.max_occupancy = form.max_occupancy.data
        room.room_size = form.room_size.data
        room.bed_type = form.bed_type.data
        room.amenities = form.amenities.data
        room.is_available = form.is_available.data
        
        db.session.add(room)
        db.session.commit()
        
        flash('Room added successfully!', 'success')
        return redirect(url_for('admin_rooms'))
    
    return render_template('admin/room_form.html', form=form, title='Add Room')

@app.route('/admin/room/<int:room_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_room(room_id):
    """Edit room"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))
    
    room = Room.query.get_or_404(room_id)
    form = RoomForm(obj=room)
    
    if form.validate_on_submit():
        room.name = form.name.data
        room.description = form.description.data
        room.price_per_night = form.price_per_night.data
        room.max_occupancy = form.max_occupancy.data
        room.room_size = form.room_size.data
        room.bed_type = form.bed_type.data
        room.amenities = form.amenities.data
        room.is_available = form.is_available.data
        
        db.session.commit()
        flash('Room updated successfully!', 'success')
        return redirect(url_for('admin_rooms'))
    
    return render_template('admin/room_form.html', form=form, title='Edit Room', room=room)

@app.route('/admin/users')
@login_required
def admin_users():
    """Admin users management (Super Admin only)"""
    if not current_user.is_admin or not current_user.is_super_admin:
        flash('Access denied. Super Admin privileges required.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/add', methods=['GET', 'POST'])
@login_required
def admin_add_user():
    """Add new admin user (Super Admin only)"""
    if not current_user.is_admin or not current_user.is_super_admin:
        flash('Access denied. Super Admin privileges required.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    form = AdminUserForm()
    if form.validate_on_submit():
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('A user with this email already exists.', 'danger')
            return render_template('admin/user_form.html', form=form, title='Add Admin User')
        
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.password_hash = generate_password_hash(form.password.data)
        user.is_admin = form.is_admin.data
        user.created_by_id = current_user.id
        
        db.session.add(user)
        db.session.commit()
        
        flash('Admin user created successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/user_form.html', form=form, title='Add Admin User')

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    """Delete admin user (Super Admin only)"""
    if not current_user.is_admin or not current_user.is_super_admin:
        flash('Access denied. Super Admin privileges required.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting the main super admin
    if user.is_super_admin and user.id != current_user.id:
        flash('Cannot delete another super admin.', 'danger')
        return redirect(url_for('admin_users'))
    
    if user.id == current_user.id:
        flash('Cannot delete yourself.', 'danger')
        return redirect(url_for('admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('Admin user deleted successfully.', 'success')
    return redirect(url_for('admin_users'))
