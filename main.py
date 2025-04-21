import pandas

df = pandas.read_csv("hotels.csv", dtype={"id": str})
df_cards = pandas.read_csv("cards.csv", dtype= str).to_dict(orient="records")


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
        if availability == "yes":
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


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_number = {"number":self.number, "expiration":expiration, "holder":holder, "cvc":cvc}
        if card_number in df_cards:
            return True
        else:
            return False
        

class Email:
    def send(self):
        pass


print(df)
hotel_ID = input("Enter the hotel id of the selected hotel: ")
hotel = Hotel(hotel_ID)
if hotel.available():
    credit_card = CreditCard(number="1234")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        hotel.book()
        name = input("Enter your name: ")
        reservation_date = input("Enter the date you want to check in: ")
        reservation_ticket = ReservationTicket(hotel_match=hotel,customer_name=name,date=reservation_date)
        print(reservation_ticket.generate())
    else:
        print("There was a problem with your payment")
else:
    print("Hotel is not available")