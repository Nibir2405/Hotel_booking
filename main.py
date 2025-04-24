import pandas
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

df = pandas.read_csv("hotels.csv", dtype={"id": str, "price_per_room":int})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """By booking a hotel, changes the hotel availability"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Checks if the hotel id is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"]
        if not availability.empty and availability.iloc[0] == "yes":
            return True
        else:
            return False
        

class SpaHotel(Hotel):
    def book_spa_package(self):
        pass


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
    def __init__(self, number, expiration, holder, cvc):
        self.number = number
        self.expiration = expiration
        self.holder = holder
        self.cvc = cvc
        
    def validate(self):
        card_number = {"number": self.number, "expiration":self.expiration, "holder": self.holder, "cvc": self.cvc}
        for card in df_cards:
            # Compare only the relevant fields, ignoring 'balance'
            if (card["number"] == card_number["number"] and
                card["expiration"] == card_number["expiration"] and
                card["holder"] == card_number["holder"] and
                card["cvc"] == card_number["cvc"]):
                return True
        return False

    def pay(self, hotel_id):
        card_number = {"number": self.number, "expiration":self.expiration, "holder": self.holder, "cvc": self.cvc}
        price = df.loc[df["id"] == hotel_id, "price_per_room"].squeeze()
        for card in df_cards:
            if (card["number"] == card_number["number"] and
                card["expiration"] == card_number["expiration"] and
                card["holder"] == card_number["holder"] and
                card["cvc"] == card_number["cvc"]):
                if int(card["balance"]) >= price:
                    card["balance"] = str(int(card["balance"]) - price)
                    pandas.DataFrame(df_cards).to_csv("cards.csv", index=False)
                    return True
        return False


class CreditCardSecurity(CreditCard):   
    def authentication(self,given_pass):
        password = df_cards_security.loc[(df_cards_security["number"] == self.number), "password"]
        if not password.empty and password.iloc[0] == given_pass:
            return True
        else:
            return False
        

class SpaTicket:
    def __init__(self,name,hotel_match):
        self.name = name
        self.hotel = hotel_match
    
    def generate(self):
        message = f"""
        Thank you for your reservation.
        Here is your Spa booking data:
        Name: {self.name}
        Hotel: {self.hotel.name}
        """
        return message

class pdf(ReservationTicket):
    def __init__(self, customer_name, date, hotel_match, spa_package):
        super().__init__(customer_name, date, hotel_match)  # Initialize the parent class
        self.spa_package = spa_package
         
    def generate(self):
        if self.spa_package == "yes":
            pdf =FPDF(orientation="P", unit="mm", format="A4")
            pdf.add_page()

            pdf.set_font(family="Times", style="B", size=16)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(w=0, h=14, txt=self.hotel.name, align="C",
                ln=1)
            pdf.line(10, 21, 200, 21)

            pdf.set_font(family="Times", size=12, style="B")
            pdf.cell(w=50, h=12, txt=f"Thank you for your reservation", ln=1)

            pdf.set_font(family="Times", size=12, style="B")
            pdf.cell(w=50, h=12, txt=f"Here is your Hotel booking data:", ln=1)

            pdf.set_font(family="Times", size=12, style="B")
            pdf.cell(w=50, h=12, txt=f"Name: {self.customer_name}", ln=1)

            pdf.set_font(family="Times", size=12, style="B")
            pdf.cell(w=50, h=12, txt=f"Check in date: {self.date}", ln=1)

            pdf.set_font(family="Times", size=12, style="B")
            pdf.cell(w=50, h=12, txt=f"You have a Spa Booking also.", ln=1)

            pdf.output("receipt.pdf")
        else:
            pdf =FPDF(orientation="P", unit="mm", format="A4")
            pdf.add_page()

            pdf.set_font(family="Times", style="B", size=16)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(w=0, h=14, txt=self.hotel.name, align="C",
                ln=1)
            pdf.line(10, 21, 200, 21)

            pdf.set_font(family="Times", size=12, style="B")
            pdf.cell(w=50, h=12, txt=f"Thank you for your reservation", ln=1)

            pdf.set_font(family="Times", size=12, style="B")
            pdf.cell(w=50, h=12, txt=f"Here is your Hotel booking data:", ln=1)

            pdf.set_font(family="Times", size=12, style="B")
            pdf.cell(w=50, h=12, txt=f"Name: {self.customer_name}", ln=1)

            pdf.set_font(family="Times", size=12, style="B")
            pdf.cell(w=50, h=12, txt=f"Check in date: {self.date}", ln=1)
            pdf.output("receipt.pdf")
        
        
        
class Email:
    def __init__(self, sender_email, sender_password, recipient_email):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email

    def send(self, subject, body, attachment_path):
        try:
            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = subject

            # Attach the email body
            msg.attach(MIMEText(body, 'plain'))

            # Attach the PDF file
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={attachment_path.split("/")[-1]}',
                )
                msg.attach(part)

            # Connect to the SMTP server and send the email
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print("A receipt of your booking has sent successfully to your email!")

        except Exception as e:
            print(f"Failed to send email: {e}")



print(df)
hotel_ID = input("Enter the hotel id of the selected hotel: ")
hotel = SpaHotel(hotel_ID)

if hotel.available():
    credit_card = CreditCardSecurity(number="1234", expiration="12/26", holder="JOHN SMITH", cvc="123")
    if credit_card.validate():
        if credit_card.authentication(given_pass="bypass"):
            if credit_card.pay(hotel_id=hotel_ID):
                hotel.book()
                name = input("Enter your name: ")
                reservation_date = input("Enter the date you want to check in: ")
                reservation_ticket = ReservationTicket(hotel_match=hotel, customer_name=name, date=reservation_date)
                print(reservation_ticket.generate())
                spa_package = input("Do you want to book a spa package? ")
                if spa_package == "yes":
                    hotel.book_spa_package()
                    spa_ticket = SpaTicket(name,hotel_match=hotel)
                    print(spa_ticket.generate())
                pdf_generate = pdf(customer_name=name,date=reservation_date,hotel_match=hotel, spa_package=spa_package)
                pdf_generate.generate()
                
                # After generating the PDF
                email = Email(sender_email="navidulislam2002@gmail.com", 
                              sender_password="eluyrpqrsoysflxj", 
                              recipient_email="nibirislam56@gmail.com")

                email.send(
                    subject="Your Hotel Booking Receipt",
                    body="Thank you for booking with us. Please find your receipt attached.",
                    attachment_path="receipt.pdf")
            else:
                print("You don't have sufficient balance")
        else:
            print("Credit card authentication failed")
    else:
        print("There was a problem with your payment")
else:
    print("Hotel is not available")