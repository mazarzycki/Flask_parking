# Parking spot reservation management

This repo has been updated to work with `Python v3.8` and up.
Requirements:
- Flask
- Flask SQLAlchemy
- datetime
- pandas
- numpy


1. The purpose of this app is to enable management of parking spots. The data is stored in sqlite database. The app was written in Flask. 

2. This server will start on port 5000 by default. You can change this in `app.py` by changing the following line to this:

```python
if __name__ == '__main__':
    app.run(debug=True, port=<desired port>)
```
3. To create a new booking there are 4 inputs to be filled: 1. desired spot number, 2. license plate of the car, 3. booking starting date and time, 4. booking end date and time.

4. After being created a booking can be removed or updated. 

5. There are 5 situations when a booking can't be created and a message will be displayed on the screen: 1. booking end time is earlier than booking start time, 2. booking start time is in the past, 3. desired booking period is shorter than 10 minutes, 4. desired spot has already been booked either for whole desired period or for part of it, 5. there is another reservation for inserted license plate for whole desired period or for part of it. For now scenarios 4 and 5 only work for creation of new bookings. They don't work for updates. 

6. Number of free spots in a given moment is displayed on the screen above the list of bookings.