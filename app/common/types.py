
from enum import Enum
from typing import TypedDict
from datetime import date

class Account(Enum):
    """Enum for different bank accounts"""
    DAVIVIENDA = "Davivienda"
    LULO = "Lulo"
    NEQUI = "Nequi"

class Movement(TypedDict):
    """
    A movement in the bank account.
    """
    id: str
    ref: str | None 
    account: Account
    date: date
    description: str
    amount: float
