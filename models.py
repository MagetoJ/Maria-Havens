from app import db
from datetime import datetime
from sqlalchemy import Text

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(Text, nullable=False)
    price_per_night = db.Column(db.Numeric(10, 2), nullable=False)
    max_occupancy = db.Column(db.Integer, nullable=False)
    room_size = db.Column(db.String(50))
    bed_type = db.Column(db.String(50))
    amenities = db.Column(Text)  # JSON string of amenities
    image_url = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Room {self.name}>'

class Amenity(db.Model):
    __tablename__ = 'amenities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # spa, dining, fitness, etc.
    image_url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Amenity {self.name}>'

class BookingInquiry(db.Model):
    __tablename__ = 'booking_inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    adults = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, default=0)
    special_requests = db.Column(Text)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    room = db.relationship('Room', backref=db.backref('inquiries', lazy=True))
    
    def __repr__(self):
        return f'<BookingInquiry {self.guest_name} - {self.check_in}>'

class ContactInquiry(db.Model):
    __tablename__ = 'contact_inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(Text, nullable=False)
    status = db.Column(db.String(20), default='new')  # new, read, replied
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactInquiry {self.name} - {self.subject}>'
