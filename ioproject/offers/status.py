from enum import Enum


class OrderStatus(Enum):
    WAITING_FOR_OFFERS = 0
    WAITING_FOR_CLIENT_DECISION = 1
    WAITING_FOR_PARTS = 2
    IN_PROGRESS = 3
    READY_TO_COLLECT = 4
    COLLECTED = 5
