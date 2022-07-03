from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pandas as pd
import numpy as np



app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking_booking.db'
db = SQLAlchemy(app)

time_now = datetime.now()

class Parking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.String(2))
    license_plate = db.Column(db.String(10))
    start = db.Column(db.String(20))
    end = db.Column(db.String(20)) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
 
    def __repr__(self):
        return '<Parking %r>' % self.id



@app.route('/', methods=['POST', 'GET'])
def index():
    
    

    if request.method == 'POST':
        booking_spot_number = str(request.form['spot_number'])
        booking_license_plate = str(request.form['license_plate'].replace(' ', '').upper())          
        booking_start = datetime(*[int(v) for v in request.form['start'].replace('T', '-').replace(':', '-').split('-')])
        booking_end = datetime(*[int(v) for v in request.form['end'].replace('T', '-').replace(':', '-').split('-')])

        df = pd.read_sql('parking', 'sqlite:///parking_booking.db')
        
        df['start'] = pd.to_datetime(df['start'])
        df['end'] = pd.to_datetime(df['end'])

        license_plate_check = np.where((df['license_plate'] == booking_license_plate) & (((df['start'] <= booking_start) & (df['end'] >= booking_start) | ((df['end'] >= booking_end) & (df['start'] <= booking_end))) | ((booking_start <= df['start']) & (booking_end >= df['end']))))
        spot_reserve_check = np.where((df['spot_number'] == booking_spot_number) & (((df['start'] <= booking_start) & (df['end'] >= booking_start) | ((df['end'] >= booking_end) & (df['start'] <= booking_end))) | ((booking_start <= df['start']) & (booking_end >= df['end']))))
        print(license_plate_check)
        print(spot_reserve_check)

        if booking_end < booking_start:
            flash('End time has to be later than start time', category='error')
        elif booking_start < datetime.now():
            flash('Start time can''t be in the past.', category='error') 
          
        elif (booking_end - booking_start) < timedelta(minutes=10):
            flash('Minimum booking time is 10 minutes.', category='error') 
        
        elif np.size(license_plate_check) != 0:
            flash(f'A car with license plate {booking_license_plate} has already booked a spot during selected time.', category='error' )

        elif np.size(spot_reserve_check) != 0:
            flash(f'The spot {booking_spot_number} has been booked during selected period.', category='error' )

        else:
            new_booking = Parking(spot_number = booking_spot_number, license_plate = booking_license_plate, start = booking_start, end = booking_end)
            db.session.add(new_booking)
            db.session.commit()
            print(df)
            flash('New booking has been added', category='success')
             
    
    bookings = Parking.query.order_by(Parking.start.asc()).all()
    return render_template('index.html', bookings = bookings)
    
@app.route('/delete/<int:id>')

def delete(id):
    item_to_delete = Parking.query.get_or_404(id)    
    db.session.delete(item_to_delete)
    db.session.commit()
    flash('Your booking has been removed', category='success')
    
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    booking = Parking.query.get_or_404(id)

    if request.method == 'POST':
        booking.spot_number = request.form['spot_number']
        booking.license_plate = request.form['license_plate']
        booking.start = datetime(*[int(v) for v in request.form['start'].replace('T', '-').replace(':', '-').split('-')])
        booking.end = datetime(*[int(v) for v in request.form['end'].replace('T', '-').replace(':', '-').split('-')]) 

        if booking.end < booking.start:
            flash('End time has to be later than start time', category='error')
        elif (booking.end - booking.start) < timedelta(minutes=10):
            flash('Minimum booking time is 10 minutes.', category='error') 
        
          
        else:
            db.session.commit() 
            flash('Your booking has been updated', category='success')    
            return redirect('/')
    return render_template('update.html', booking = booking)


if __name__ == '__main__':
    app.run(debug=True)
