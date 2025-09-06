#!/usr/bin/env python3
"""
Database initialization script for Maria Havens
Run this script to populate the database with sample data
"""

import os
import sys
from datetime import datetime, date
from decimal import Decimal

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Room, Amenity, BookingInquiry, ContactInquiry, User
from werkzeug.security import generate_password_hash

def create_sample_rooms():
    """Create sample room data"""
    rooms = [
        {
            'name': 'Deluxe Ocean View',
            'description': 'Elegant room featuring stunning ocean views, premium furnishings, and modern amenities. Perfect for couples seeking a romantic getaway with breathtaking sunset views from the private balcony.',
            'price_per_night': Decimal('299.00'),
            'max_occupancy': 2,
            'room_size': '450 sq ft',
            'bed_type': 'King Bed',
            'amenities': 'Ocean view, Private balcony, Mini-bar, Smart TV, Premium bedding, Coffee maker, Safe'
        },
        {
            'name': 'Family Suite',
            'description': 'Spacious two-bedroom suite ideal for families, featuring separate living area, kitchenette, and kid-friendly amenities. Enjoy quality family time with comfort and convenience.',
            'price_per_night': Decimal('449.00'),
            'max_occupancy': 6,
            'room_size': '750 sq ft',
            'bed_type': '1 King + 2 Twin Beds',
            'amenities': 'Kitchenette, Living area, Two bathrooms, Kids amenities, Sofa bed, Dining table'
        },
        {
            'name': 'Presidential Suite',
            'description': 'The epitome of luxury featuring panoramic views, marble bathrooms, separate dining area, and exclusive concierge service. Experience unparalleled comfort and sophistication.',
            'price_per_night': Decimal('899.00'),
            'max_occupancy': 4,
            'room_size': '1200 sq ft',
            'bed_type': 'King Bed + Sofa Bed',
            'amenities': 'Panoramic views, Marble bathroom, Dining area, Premium bar, Butler service, Private terrace'
        },
        {
            'name': 'Garden View Room',
            'description': 'Tranquil room overlooking our beautifully landscaped gardens, offering a peaceful retreat with modern comforts and easy access to hotel amenities.',
            'price_per_night': Decimal('229.00'),
            'max_occupancy': 2,
            'room_size': '400 sq ft',
            'bed_type': 'Queen Bed',
            'amenities': 'Garden view, Work desk, Mini-fridge, Smart TV, Premium Wi-Fi, Rain shower'
        },
        {
            'name': 'Spa Wellness Suite',
            'description': 'Rejuvenating suite designed for wellness enthusiasts, featuring in-room spa amenities, meditation area, and direct access to our world-class spa facilities.',
            'price_per_night': Decimal('649.00'),
            'max_occupancy': 2,
            'room_size': '600 sq ft',
            'bed_type': 'King Bed',
            'amenities': 'Spa access, Meditation area, Aromatherapy, Yoga mat, Healthy mini-bar, Deep soaking tub'
        }
    ]
    
    for room_data in rooms:
        existing_room = Room.query.filter_by(name=room_data['name']).first()
        if not existing_room:
            room = Room(**room_data)
            db.session.add(room)
    
    db.session.commit()
    print(f"Created {len(rooms)} sample rooms")

def create_sample_amenities():
    """Create sample amenity data"""
    amenities = [
        {
            'name': 'Serenity Spa',
            'description': 'Award-winning spa offering therapeutic massages, rejuvenating facials, and holistic wellness treatments in a tranquil setting.',
            'category': 'spa'
        },
        {
            'name': 'Infinity Pool',
            'description': 'Stunning infinity pool overlooking the ocean with poolside service, comfortable loungers, and cabana rentals available.',
            'category': 'pool'
        },
        {
            'name': 'Azure Restaurant',
            'description': 'Fine dining restaurant featuring contemporary cuisine, fresh seafood, and an extensive wine collection with ocean views.',
            'category': 'dining'
        },
        {
            'name': 'Fitness Center',
            'description': 'State-of-the-art fitness facility with modern equipment, personal training services, and group fitness classes.',
            'category': 'fitness'
        },
        {
            'name': 'Beach Club',
            'description': 'Private beach access with water sports equipment, beach volleyball, and beachside refreshments.',
            'category': 'recreation'
        },
        {
            'name': 'Poolside Grill',
            'description': 'Casual dining venue offering grilled specialties, tropical cocktails, and light bites in a relaxed poolside atmosphere.',
            'category': 'dining'
        },
        {
            'name': 'Yoga Pavilion',
            'description': 'Open-air pavilion hosting daily yoga sessions, meditation classes, and wellness workshops with ocean views.',
            'category': 'wellness'
        },
        {
            'name': 'Business Center',
            'description': 'Fully equipped business center with meeting rooms, conference facilities, and high-speed internet for corporate guests.',
            'category': 'business'
        },
        {
            'name': 'Kids Club',
            'description': 'Supervised activities and entertainment for children, featuring games, crafts, and educational programs.',
            'category': 'family'
        },
        {
            'name': 'Tennis Court',
            'description': 'Professional tennis court with equipment rental and lessons available from certified instructors.',
            'category': 'recreation'
        }
    ]
    
    for amenity_data in amenities:
        existing_amenity = Amenity.query.filter_by(name=amenity_data['name']).first()
        if not existing_amenity:
            amenity = Amenity(**amenity_data)
            db.session.add(amenity)
    
    db.session.commit()
    print(f"Created {len(amenities)} sample amenities")

def create_main_admin():
    """Create the main admin user"""
    # Check if main admin already exists
    existing_admin = User.query.filter_by(email='jabezmageto78@gmail.com').first()
    if not existing_admin:
        main_admin = User(
            email='jabezmageto78@gmail.com',
            password_hash=generate_password_hash('lokeshen@58'),
            name='Jabez Mageto',
            is_admin=True,
            is_super_admin=True  # This is the manager who can create other admins
        )
        db.session.add(main_admin)
        db.session.commit()
        print("Created main admin user: jabezmageto78@gmail.com")
    else:
        print("Main admin user already exists")

def main():
    """Main function to initialize database with sample data"""
    with app.app_context():
        print("Initializing database for Maria Havens...")
        
        # Create all tables
        db.create_all()
        print("Database tables created successfully")
        
        # Create sample data
        create_sample_rooms()
        create_sample_amenities()
        create_main_admin()
        
        print("\nDatabase initialization completed successfully!")
        print("You can now run the application with: python main.py")
        
        # Display summary
        room_count = Room.query.count()
        amenity_count = Amenity.query.count()
        user_count = User.query.count()
        
        print(f"\nDatabase Summary:")
        print(f"- Rooms: {room_count}")
        print(f"- Amenities: {amenity_count}")
        print(f"- Admin Users: {user_count}")
        print(f"- Booking Inquiries: 0")
        print(f"- Contact Inquiries: 0")

if __name__ == '__main__':
    main()
