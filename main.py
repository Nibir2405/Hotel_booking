import pandas

df = pandas.read_csv("hotels.csv", dtype={"id": str})



class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id

    def book(self):
        """By booking a hotels,changes the hotel availability"""
        df.loc[df["id"]==self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Checks if the hotel id is available"""
        availability = df.loc[df["id"]==self.hotel_id, "available"]
        if availability.iloc[0]== "yes":
            return True
        else:
            return False
        

class ReservationTicket:
    def __init__(self, customer_name, date, hotel_match):
        pass
    def generate(self):
        pass


class Email:
    def send(self):
        pass


print(df)
hotel_ID = input("Enter the hotel id of the selected hotel: ")
hotel = Hotel(hotel_ID)
if hotel.available():
    hotel.book()
    name = input("Enter your name: ")
    reservation_date = input("Enter the date you want to stay in the hotel: ")
    reservation_ticket = ReservationTicket(name, reservation_date, hotel)
