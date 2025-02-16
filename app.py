from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db = SQLAlchemy(app)

# Database Model for Bookings
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_number = db.Column(db.String(10), unique=True, nullable=False)  # UNIQUE prevents double booking

# Create the database
with app.app_context():
    db.create_all()

# Home Page
@app.route('/')
def home():
    return "Welcome to the Library Booking System!"



# View All Bookings
@app.route('/book', methods=['GET', 'POST'])
def book_seat():
    all_seats = ['1A', '1B', '2A', '2B', '3A', '3B']  # List of all seats
    booked_seats = [b.seat_number for b in Booking.query.all()]  # Get booked seats from DB
    available_seats = [seat for seat in all_seats if seat not in booked_seats]  # Find free seats

    if request.method == 'POST':
        seat_number = request.form['seat']
        if seat_number in booked_seats:
            return f"Sorry, seat {seat_number} is already booked! Try another one."
        
        new_booking = Booking(seat_number=seat_number)
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('book_seat'))

    return render_template('book.html', available_seats=available_seats)

    app.run(debug=True)


    if request.method == 'POST':
        seat_number = request.form['seat']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']

        # Check if seat is already booked for the selected date/time
        existing_booking = Booking.query.filter_by(seat_number=seat_number, date=date, time=time).first()
        if existing_booking:
            return "Seat already booked for this time!"

        new_booking = Booking(seat_number=seat_number, email=email, date=date, time=time)
        db.session.add(new_booking)
        db.session.commit()

        send_confirmation_email(email, seat_number)
        return redirect(url_for('book_seat'))

    return render_template('book.html')

    booking = Booking.query.get(booking_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
    return redirect(url_for('view_bookings'))




