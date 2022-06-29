from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking_booking.db'
db = SQLAlchemy(app)

class Parking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.String(2), nullable=False)
    license_plate = db.Column(db.String(10), nullable=False)
    start = db.Column(db.String(20))
    end = db.Column(db.String(20)) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Parking %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        booking_spot_number = request.form['spot_number']
        booking_license_plate = request.form['license_plate'].upper()          
        booking_start = datetime(*[int(v) for v in request.form['start'].replace('T', '-').replace(':', '-').split('-')])
        booking_end = datetime(*[int(v) for v in request.form['end'].replace('T', '-').replace(':', '-').split('-')])    

        if booking_end < booking_start:
            flash('End time has to be later than start time', category='error')
            
        else:
            new_booking = Parking(spot_number = booking_spot_number, license_plate = booking_license_plate, start = booking_start, end = booking_end)
            db.session.add(new_booking)
            db.session.commit()
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
        booking.start = request.form['start']
        booking.end = request.form['end']  

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your booking.'

    else:
        return render_template('update.html', booking = booking )


if __name__ == '__main__':
    app.run(debug=True)
