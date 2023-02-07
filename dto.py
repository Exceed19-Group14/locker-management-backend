from datetime import datetime
from pydantic import BaseModel, validator
from typing import List, Dict, Union


class CreateLockerTransaction(BaseModel):
    nisit_id: str
    locker_number: int
    expected_date: datetime
    store: Dict[str, List[str]]
    
    @validator("locker_number")
    def check_locker_number(self, locker_number: int):
        if locker_number not in range(1, 7):
            raise ValueError("locker number not in range of 6")
        return locker_number

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
