from flask import Flask, render_template, request, redirect, flash
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

class Reservation:
    def __init__(self, spot_number, license_plate, start, end):
        self.spot_number = spot_number
        self.license_plate = license_plate
        self.start = start 
        self.end = end

    #def validate_license_plate(self, df):
     #   return np.where((df['license_plate'] == self.license_plate) & (((df['start'] <= self.start) & (df['end'] >= self.start) | ((df['end'] >= self.end) & (df['start'] <= self.end))) | ((self.start <= df['start']) & (self.end >= df['end']))))
        
    #def validate_spot_already_booked(self, df):
     #   return np.where((df['spot_number'] == self.spot_number) & (((df['start'] <= self.start) & (df['end'] >= self.start) | ((df['end'] >= self.end) & (df['start'] <= self.end))) | ((self.start <= df['start']) & (self.end >= df['end']))))

    def validate(self, df):
        if self.end < self.start:
            return 'End time has to be later than start time'
        elif self.start < datetime.now():
            return 'Start time can''t be in the past.' 
        elif (self.end - self.start) < timedelta(minutes=10):
            return 'Minimum booking time is 10 minutes.'
        #elif np.size((df['license_plate'] == self.license_plate) & (((df['start'] <= self.start) & (df['end'] >= self.start) | ((df['end'] >= self.end) & (df['start'] <= self.end))) | ((self.start <= df['start']) & (self.end >= df['end']))) > 0):
         #   return f'A car with license plate {self.license_plate} has already booked a spot during selected time.'
        #elif np.size((df['spot_number'] == self.spot_number) & (((df['start'] <= self.start) & (df['end'] >= self.start) | ((df['end'] >= self.end) & (df['start'] <= self.end))) | ((self.start <= df['start']) & (self.end >= df['end']))) > 0):
         #   return f'The spot {self.spot_number} has been booked during selected period.'
        else:
            return ''
    
@app.route('/', methods=['POST', 'GET'])
def index():
    df = pd.read_sql('parking', 'sqlite:///parking_booking.db')
    df['start'] = pd.to_datetime(df['start'])
    df['end'] = pd.to_datetime(df['end'])
    print(df.shape)

    bookings = Parking.query.order_by(Parking.start.asc()).all()
    time_now = str(datetime.now().strftime('%a %d %b %Y - %H:%M'))
    free_spots = 10 - np.size(np.where((time_now >= df['start']) & (time_now <= df['end'])))

    if request.method == 'POST':

        R = Reservation(str(request.form['spot_number']), str(request.form['license_plate'].replace(' ', '').upper()), datetime(*[int(v) for v in request.form['start'].replace('T', '-').replace(':', '-').split('-')]), datetime(*[int(v) for v in request.form['end'].replace('T', '-').replace(':', '-').split('-')]))
        
        license_plate_check = np.where((df['license_plate'] == R.license_plate) & (((df['start'] <= R.start) & (df['end'] >= R.start) | ((df['end'] >= R.end) & (df['start'] <= R.end))) | ((R.start <= df['start']) & (R.end >= df['end']))))
        spot_reserve_check = np.where((df['spot_number'] == R.spot_number) & (((df['start'] <= R.start) & (df['end'] >= R.start) | ((df['end'] >= R.end) & (df['start'] <= R.end))) | ((R.start <= df['start']) & (R.end >= df['end']))))

                
        message = R.validate(df)
        if not message == '':
            flash(message, category='error')
        elif np.size(license_plate_check) != 0:
            
            flash(f'A car with license plate {R.license_plate} has already booked a spot during selected time.', category='error' )

        elif np.size(spot_reserve_check) != 0:
            
            flash(f'The spot {R.spot_number} has been booked during selected period.', category='error' )
        else:
            new_booking = Parking(spot_number = R.spot_number, license_plate = R.license_plate, start = R.start, end = R.end)
            db.session.add(new_booking)
            db.session.commit()
            bookings = Parking.query.order_by(Parking.start.asc()).all()
            flash('New booking has been added', category='success') 
    
    return render_template('index.html', bookings = bookings, time_now = time_now , free_spots = free_spots)

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
        booking.spot_number = str(request.form['spot_number'])
        booking.license_plate = str(request.form['license_plate'].replace(' ', '').upper())          
        booking.start = datetime(*[int(v) for v in request.form['start'].replace('T', '-').replace(':', '-').split('-')])
        booking.end = datetime(*[int(v) for v in request.form['end'].replace('T', '-').replace(':', '-').split('-')])

        df = pd.read_sql('parking', 'sqlite:///parking_booking.db')
        
        df['start'] = pd.to_datetime(df['start'])
        df['end'] = pd.to_datetime(df['end'])

        license_plate_check = np.where((df['license_plate'] == booking.license_plate) & (((df['start'] <= booking.start) & (df['end'] >= booking.start) | ((df['end'] >= booking.end) & (df['start'] <= booking.end))) | ((booking.start <= df['start']) & (booking.end >= df['end']))))
        spot_reserve_check = np.where((df['spot_number'] == booking.spot_number) & (((df['start'] <= booking.start) & (df['end'] >= booking.start) | ((df['end'] >= booking.end) & (df['start'] <= booking.end))) | ((booking.start <= df['start']) & (booking.end >= df['end']))))

        if booking.end < booking.start:
            flash('End time has to be later than start time', category='error')

        elif (booking.end - booking.start) < timedelta(minutes=10):
            flash('Minimum booking time is 10 minutes.', category='error')

        elif np.size(license_plate_check) != 0:
            
            flash(f'A car with license plate {booking.license_plate} has already booked a spot during selected time.', category='error' )

        elif np.size(spot_reserve_check) != 0:
            
            flash(f'The spot {booking.spot_number} has been booked during selected period.', category='error' )
 
        else:
            db.session.commit() 
            flash('Your booking has been updated', category='success')    
            return redirect('/')
    return render_template('update.html', booking = booking)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
