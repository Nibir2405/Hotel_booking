import pandas

df = pandas.read_csv("hotels.csv", dtype={"id": str})



class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"]==self.hotel_id, "name"].squeeze()

    def book(self):
        """By booking a hotels,changes the hotel availability"""
        df.loc[df["id"]==self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Checks if the hotel id is available"""
        availability = df.loc[df["id"]==self.hotel_id, "available"].squeeze()
        if availability.iloc[0]== "yes":
            return True
        else:
            return False
        

class ReservationTicket:
    def __init__(self, customer_name, date, hotel_match):
        self.customer_name = customer_name
        self.date = date
        self.hotel = hotel_match
    def generate(self):
        content = f"""
        Thank you for your reservation.
        Here is your booking data:
        Name: {self.customer_name}
        Hotel: {self.hotel.name}
        Check in: {self.date}
        """
        return content

class Email:
    def send(self):
        pass


print(df)
hotel_ID = input("Enter the hotel id of the selected hotel: ")
hotel = Hotel(hotel_ID)
if hotel.available():
    hotel.book()
    name = input("Enter your name: ")
    reservation_date = input("Enter the date you want to check in: ")
    reservation_ticket = ReservationTicket(hotel_match=hotel,customer_name=name,date=reservation_date)
    print(reservation_ticket.generate())

else:
    print("Hotel is not available")