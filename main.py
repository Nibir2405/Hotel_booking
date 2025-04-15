import pandas

df = pandas.read_csv("hotels.csv")



class Hotel:
    def __init__(self,id):
        pass

    def book(self):
        pass

    def available(self):
        pass

class ReservationTicket:
    def __init__(self, customer_name, date, hotel_match):
        pass
    def generate(self):
        pass


class Email:
    def send(self):
        pass


print(df)
id = input("Enter the hotel id of the selected hotel: ")
hotel = Hotel(id)
if hotel.available():
    hotel.book()
    name = input("Enter your name: ")
    reservation_date = input("Enter the date you want to stay in the hotel: ")
    reservation_ticket = ReservationTicket(name, reservation_date, hotel)
