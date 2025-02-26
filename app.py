from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress a warning
db = SQLAlchemy(app)

# Database Model for Bookings
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seat_number = db.Column(db.String(10), unique=True, nullable=False)  # UNIQUE prevents double booking
    email = db.Column(db.String(100), nullable=True)  # Optional: Add email for confirmation
    date = db.Column(db.String(20), nullable=True)  # Optional: Add date for booking
    time = db.Column(db.String(20), nullable=True)  # Optional: Add time for booking

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
        email = request.form.get('email')  # Optional: Get email from form
        date = request.form.get('date')  # Optional: Get date from form
        time = request.form.get('time')  # Optional: Get time from form

        # Check if seat is already booked
        existing_booking = Booking.query.filter_by(seat_number=seat_number).first()
        if existing_booking:
            return f"Sorry, seat {seat_number} is already booked! Try another one."

        # Create a new booking
        new_booking = Booking(seat_number=seat_number, email=email, date=date, time=time)
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('book_seat'))

    return render_template('book.html', available_seats=available_seats)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)



from flask_mail import Mail, Message

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
mail = Mail(app)

# Function to send confirmation email
def send_confirmation_email(email, seat_number):
    msg = Message('Library Seat Booking Confirmation',
                  sender='your-email@gmail.com',
                  recipients=[email])
    msg.body = f'Your seat {seat_number} has been successfully booked!'
    mail.send(msg)