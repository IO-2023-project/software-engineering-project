import smtplib
import ssl
from email.message import EmailMessage


# TODO: dodać link do strony z logowaniem dla kliena
LOGIN_CUSTOMER_PAGE = "TODO"  # nie wiem jaki ma być link


def send_email(receiver_email: str, msg: EmailMessage) -> None:
    """
    Sends e-mail to given receiver\n
    :param receiver_email: receiver's e-mail address
    :param msg: EmailMessage with set subject and body (content)
    """
    port = 465  # For SSL

    credentials = open("credentials.txt", 'r')  # login information
    sender_email = credentials.readline().split()[0]
    password = credentials.readline().split()[0]

    msg['From'] = sender_email
    msg["To"] = receiver_email

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)

        server.sendmail(sender_email, receiver_email, msg.as_string())


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

    body = f"Zlecenie dotyczące pojazdu o numerze rejestracyjnym {registration_number} zostało utworzone.\n"
    f"Możesz śledzić postępy korzystając z podanego linku:\n\t{link}\n"
    f"lub zalogować się na stronie:\n\t{LOGIN_CUSTOMER_PAGE}\n"
    f"za pomocą id zlecenia:\n\t{order_id}\n\n"
    f"Twój Pan Mechanik"

    msg.set_content(body)

    send_email(customer_email, msg)


# przykład wywołania
# send_new_order_email("twoj.najulubienszy.mechanik@gmail.com", "https://tenor.com/pl/view/cheers-raise-your-glass-gentlemen-nice-clapping-gif-5555911", 0, "KK 678J")
