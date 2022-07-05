from app import *

def test_reservation_is_ok():
    R = Reservation('A2', 'G972', datetime(2022, 8, 4, 21, 20), datetime(2022, 8, 4, 22, 00))
    df = pd.DataFrame(columns = ['spot_number', 'license_plate', 'start', 'end'])
    message = R.validate(df)

    assert message == '', message

def test_duration_less_than_10_min():
    R = Reservation('A2', 'GR972', datetime(2022, 8, 4, 21, 20), datetime(2022, 8, 4, 21, 25))
    df = pd.DataFrame(columns = ['spot_number', 'license_plate', 'start', 'end'])
    message = R.validate(df)

    assert message == 'Minimum booking time is 10 minutes.', message

def test_end_before_start():
    R = Reservation('A2', 'GR972', datetime(2022, 8, 4, 21, 25), datetime(2022, 8, 4, 21, 20))
    df = pd.DataFrame(columns = ['spot_number', 'license_plate', 'start', 'end'])
    message = R.validate(df)

    assert message == 'End time has to be later than start time', message

def test_license_plate_exists_inside_time():
      R = Reservation('A2', 'GR972', datetime(2022, 8, 4, 21, 00), datetime(2022, 8, 4, 22, 00))
      df = pd.DataFrame(data = {'spot_number' : ['A1'], 'license_plate' : ['GR972'], 'start': datetime(2022, 8, 4, 21, 10), 'end' : datetime(2022, 8, 4, 21, 40)})

      array = (df['license_plate'] == R.license_plate) & (((df['start'] <= R.start) & (df['end'] >= R.start) | ((df['end'] >= R.end) & (df['start'] <= R.end))) | ((R.start <= df['start']) & (R.end >= df['end'])))
      assert np.size(array) != 0

def test_license_plate_exists_outside_time():
      R = Reservation('A2', 'GR972', datetime(2022, 8, 4, 21, 00), datetime(2022, 8, 4, 22, 00))
      df = pd.DataFrame(data = {'spot_number' : ['A1'], 'license_plate' : ['GR972'], 'start': datetime(2022, 8, 4, 20, 10), 'end' : datetime(2022, 8, 4, 22, 40)})

      array = (df['license_plate'] == R.license_plate) & (((df['start'] <= R.start) & (df['end'] >= R.start) | ((df['end'] >= R.end) & (df['start'] <= R.end))) | ((R.start <= df['start']) & (R.end >= df['end'])))
      assert np.size(array) != 0

def test_license_plate_exists_start_outside_time():
      R = Reservation('A2', 'GR972', datetime(2022, 8, 4, 21, 00), datetime(2022, 7, 4, 22, 00))
      df = pd.DataFrame(data = {'spot_number' : ['A1'], 'license_plate' : ['GR972'], 'start': datetime(2022, 8, 4, 20, 10), 'end' : datetime(2022, 8, 4, 21, 40)})

      array = (df['license_plate'] == R.license_plate) & (((df['start'] <= R.start) & (df['end'] >= R.start) | ((df['end'] >= R.end) & (df['start'] <= R.end))) | ((R.start <= df['start']) & (R.end >= df['end'])))
      assert np.size(array) != 0

def test_license_plate_exists_end_outside_time():
      R = Reservation('A2', 'GR972', datetime(2022, 8, 4, 21, 00), datetime(2022, 7, 4, 22, 00))
      df = pd.DataFrame(data = {'spot_number' : ['A1'], 'license_plate' : ['GR972'], 'start': datetime(2022, 8, 4, 21, 10), 'end' : datetime(2022, 8, 4, 22, 40)})

      array = (df['license_plate'] == R.license_plate) & (((df['start'] <= R.start) & (df['end'] >= R.start) | ((df['end'] >= R.end) & (df['start'] <= R.end))) | ((R.start <= df['start']) & (R.end >= df['end'])))
      assert np.size(array) != 0


def test_spot_booked_inside_time():
      R = Reservation('A2', 'GR972', datetime(2022, 8, 4, 21, 00), datetime(2022, 7, 4, 22, 00))
      df = pd.DataFrame(data = {'spot_number' : ['A2'], 'license_plate' : ['GA045'], 'start': datetime(2022, 8, 4, 21, 10), 'end' : datetime(2022, 8, 4, 21, 40)})

      array = (df['license_plate'] == R.license_plate) & (((df['start'] <= R.start) & (df['end'] >= R.start) | ((df['end'] >= R.end) & (df['start'] <= R.end))) | ((R.start <= df['start']) & (R.end >= df['end'])))
      assert np.size(array) != 0

def test_spot_booked_outside_time():
      R = Reservation('A2', 'GR972', datetime(2022, 8, 4, 21, 00), datetime(2022, 7, 4, 22, 00))
      df = pd.DataFrame(data = {'spot_number' : ['A2'], 'license_plate' : ['GA045'], 'start': datetime(2022, 8, 4, 20, 10), 'end' : datetime(2022, 8, 4, 22, 40)})

      array = (df['license_plate'] == R.license_plate) & (((df['start'] <= R.start) & (df['end'] >= R.start) | ((df['end'] >= R.end) & (df['start'] <= R.end))) | ((R.start <= df['start']) & (R.end >= df['end'])))
      assert np.size(array) != 0

def test_spot_booked_start_outside_time():
      R = Reservation('A2', 'GR972', datetime(2022, 8, 4, 21, 00), datetime(2022, 7, 4, 22, 00))
      df = pd.DataFrame(data = {'spot_number' : ['A2'], 'license_plate' : ['GA045'], 'start': datetime(2022, 8, 4, 20, 10), 'end' : datetime(2022, 8, 4, 21, 40)})

      array = (df['license_plate'] == R.license_plate) & (((df['start'] <= R.start) & (df['end'] >= R.start) | ((df['end'] >= R.end) & (df['start'] <= R.end))) | ((R.start <= df['start']) & (R.end >= df['end'])))
      assert np.size(array) != 0

def test_spot_booked_end_outside_time():
      R = Reservation('A2', 'GR972', datetime(2022, 8, 4, 21, 00), datetime(2022, 7, 4, 22, 00))
      df = pd.DataFrame(data = {'spot_number' : ['A2'], 'license_plate' : ['GA045'], 'start': datetime(2022, 8, 4, 21, 10), 'end' : datetime(2022, 8, 4, 22, 40)})

      array = (df['license_plate'] == R.license_plate) & (((df['start'] <= R.start) & (df['end'] >= R.start) | ((df['end'] >= R.end) & (df['start'] <= R.end))) | ((R.start <= df['start']) & (R.end >= df['end'])))
      assert np.size(array) != 0




