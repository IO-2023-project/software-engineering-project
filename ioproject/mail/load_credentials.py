from ioproject.settings import BASE_DIR


CREDENTIALS_DIR = BASE_DIR / "mail" / "credentials.txt"


def load_credentials():
    credentials = open(CREDENTIALS_DIR, 'r')  # login information
    sender_email = credentials.readline().split()[0]
    password = credentials.readline().split()[0]
    credentials.close()

    return sender_email, password
