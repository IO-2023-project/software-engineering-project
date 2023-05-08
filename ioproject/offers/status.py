from enum import Enum


class OrderStatus(Enum):
    WAITING_FOR_OFFERS = 0
    WAITING_FOR_CLIENT_DECISION = 1
    WAITING_FOR_PARTS = 2
    IN_PROGRESS = 3
    READY_TO_COLLECT = 4
    COLLECTED = 5

    def __str__(self):
        if self.value == 0:
            return "Oczekiwanie na oferty mechanika"
        elif self.value == 1:
            return "Oczekiwanie na decyzję klienta"
        elif self.value == 2:
            return "Oczekiwanie na części"
        elif self.value == 3:
            return "W trakcie naprawy"
        elif self.value == 4:
            return "Gotowy do odbioru"
        elif self.value == 5:
            return "Odebrany"