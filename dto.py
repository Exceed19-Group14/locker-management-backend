from datetime import datetime
from pydantic import BaseModel
from typing import List, Dict, Union


class CreateLockerTransaction(BaseModel):
    nisit_id: str
    locker_number: int
    expected_date: datetime
    store: Dict[str, List[str]]


class LockerTransaction(CreateLockerTransaction):
    initial_date: datetime
    withdraw_date: Union[datetime, None] = None


class Locker(BaseModel):
    locker_number: int
    is_avaliable: bool


class TotalPayment(BaseModel):
    nisit_id: str
    total_payment: int


class Payment(BaseModel):
    price: int


class Receipt(TotalPayment):
    cash: int
    change: int
