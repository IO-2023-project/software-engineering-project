import smtplib
import ssl
from email.message import EmailMessage

from ioproject.settings import DOMAIN_ADDRESS
from mail.load_credentials import load_credentials

from offers.models import ClientOrder, MechanicOffer, OrderStatus

# TODO: dodać link do strony z logowaniem dla kliena
LOGIN_CUSTOMER_PAGE = "TODO: link do strony ze sprawdzaniem zamówień"  # nie wiem jaki ma być link
SENDER_EMAIL, PASSWORD = load_credentials()


def send_email(receiver_email: str, msg: EmailMessage) -> None:
    """
    Sends e-mail to given receiver\n
    :param receiver_email: receiver's e-mail address
    :param msg: EmailMessage with set subject and body (content)
    """
    port = 465  # For SSL

    msg['From'] = SENDER_EMAIL
    msg["To"] = receiver_email

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)

        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())


def send_new_order_email(customer_email: str, link: str, order_id: int, registration_number: str) -> None:
    """
    Sends e-mail to the given customer e-mail address about new customer's order
    :param customer_email: customer e-mail address
    :param link: link to the new customer order main page
    :param order_id: id of the new customer order
    :param registration_number: registration number of customer's car
    """

    msg = EmailMessage()

    msg["Subject"] = f"Mechanik - Potwierdzenie utworzenia zlecenia"

    body = (f"Zlecenie dotyczące pojazdu o numerze rejestracyjnym {registration_number} zostało utworzone.\n"
            f"Możesz śledzić postępy korzystając z podanego linku:\n\t{link}\n"
            f"lub zalogować się na stronie:\n\t{LOGIN_CUSTOMER_PAGE}\n"
            f"za pomocą id zlecenia:\n\t{order_id}\n\n"
            f"Twój Pan Mechanik")

    msg.set_content(body)

    send_email(customer_email, msg)


def send_email_about_created_offers(order_id: int):
    order = ClientOrder.objects.get(id=order_id)

    email = order.email

    registration_number = order.registration_number

    link = DOMAIN_ADDRESS + "orders/" + str(order_id) + "/view_offer"

    msg = EmailMessage()

    msg["Subject"] = f"Mechanik - proponowane oferty"

    body = (f"Zlecenie dotyczące pojazdu o numerze rejestracyjnym {registration_number} zostało zaktualizowane.\n"
            f"Możesz wybrać ofertę serwisu pojazdu pod tym linkiem:\n\t{link}\n\n"
            # f"lub zalogować się na stronie:\n\t{LOGIN_CUSTOMER_PAGE}\n"
            # f"za pomocą id zlecenia:\n\t{order_id}\n\n"
            f"Twój Pan Mechanik")

    msg.set_content(body)

    send_email(email, msg)


def email_about_chosen_offer(order_id: int, offer_id: int):
    registration_number = ClientOrder.objects.get(id=order_id).registration_number
    offer_name = MechanicOffer.objects.get(id=offer_id).offer_content

    msg = EmailMessage()

    msg["Subject"] = f"Zlecenie {order_id}: wybrano ofertę"

    body = (f"Klient wybrał ofetę:\n"
            f"\tZlecenie nr {order_id} dotyczące pojazdu o numerze rejestracyjnym {registration_number}.\n"
            f"\tWybrano:\n"
            f"\t\tOferta nr {offer_id}: {offer_name}\n")

    msg.set_content(body)

    mechanic_email = SENDER_EMAIL

    send_email(mechanic_email, msg)

