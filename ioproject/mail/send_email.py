import smtplib
import ssl
from email.message import EmailMessage


# TODO: dodać link do strony z logowaniem dla kliena
LOGIN_CLIENT_PAGE = "TODO"  # nie wiem jaki ma być link


def send_email(receiver_email: str, msg: "email.message.EmailMessage") -> None:
    port = 465  # For SSL

    credentials = open("credentials.txt", 'r')
    sender_email = credentials.readline().split()[0]
    password = credentials.readline().split()[0]

    msg['From'] = sender_email
    msg["To"] = receiver_email

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)

        server.sendmail("twoj.najulubienszy.mechanik@gmail.com", receiver_email, msg.as_string())


def send_new_commission_mail(client_mail: str, link: str, commission_id: int, registration_number: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = f"Mechanik - Potwierdzenie utworzenia zlecenia"
    body = f"""
    Zlecenie dotyczące pojazdu o numerze rejestracyjnym {registration_number} zostało utworzone.
    Możesz śledzić postępy korzystając z podanego linku:\n {link}
    lub zalogować się na stronie:\n {LOGIN_CLIENT_PAGE}
    za pomocą id zlecenia:\n {commission_id}\n
    Twój Pan Mechanik
    """
    msg.set_content(body)

    send_email(client_mail, msg)


# przykład wywołania
# send_new_commission_mail("twoj.najulubienszy.mechanik@gmail.com", "https://tenor.com/pl/view/cheers-raise-your-glass-gentlemen-nice-clapping-gif-5555911", 0, "KK 678J")
