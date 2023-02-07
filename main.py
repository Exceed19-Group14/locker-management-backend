from datetime import datetime, timedelta
from fastapi import FastAPI
from database.db import collection
from dto import CreateLockerTransaction, LockerTransaction
import math

app = FastAPI()

def calculate_payment(dto: LockerTransaction) -> int:
    pass

def is_locker_available(dto: CreateLockerTransaction) -> bool:
    pass

@app.get('/')
def root():
    return {"msg": "welcome to locker reservation system"}

@app.post('/locker/deposit')
def deposit_item(dto: CreateLockerTransaction):
    doc = dto.dict()
    doc['initial_date'] = datetime.now()
    doc['withdraw_date'] = None

@app.get('/locker/payment/{nisit_id}')
def show_payment(nisit_id: str):
    return {"total payment": collection.find_one({"nisit_id": nisit_id, "is_payment": False},
                                                 {"price": 1})}

@app.put('/locker/withdraw/{nisit_id}')
def withdraw_item(nisit_id: str):
    order = collection.find_one({"nisit_id": nisit_id, "is_payment": False})
    actual_withdraw_time = datetime.now()
    if (order.expect_date - order.initial_date > timedelta(hours=2)):
        total_payment = 5 * math.ceil(
            (order.expect_date - order.initial_date - timedelta(hours=2)).seconds/3600)
    else:
        total_payment = 0
    # add fee
    if (actual_withdraw_time > order.expect_date):
        total_payment += 20 * math.ceil(
            (actual_withdraw_time - order.expect_date).seconds/600)
    collection.update_one(order, {"withdraw_date": datetime.now(), 
                                  "price": total_payment})
    


