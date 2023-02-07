from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, status, Body
from database.db import collection
from dto import CreateLockerTransaction, Locker, TotalPayment, Receipt, Payment
import math

app = FastAPI()

lockers = [i for i in range(1, 7)]


def calculate_payment(expected_date: datetime, initial_date: datetime) -> int:
    if (expected_date - initial_date > timedelta(hours=2)):
        return 5 * math.ceil(
            (expected_date - initial_date - timedelta(hours=2)).seconds/3600)
    else:
        return 0


def calculate_fee(expected_date: datetime, withdraw_date: datetime) -> int:
    if (withdraw_date > expected_date):
        return 20 * math.ceil(
            (withdraw_date - expected_date).seconds/600)
    return 0


@app.get('/')
def root():
    return {"msg": "welcome to locker reservation system"}


@app.post('/locker/deposit')
def deposit_item(dto: CreateLockerTransaction):
    doc = dto.dict()
    doc['initial_date'] = datetime.now()
    doc['withdraw_date'] = None
    doc['price'] = None
    doc['is_payment'] = False
    collection.insert_one(doc)


@app.get('/locker/{id}')
def locker_info(id: int):
    if not id in lockers:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {
            "error": "Locker must be more than or equal 1 and less than or equal 6"
        })
    count = collection.count_documents({
        "locker_number": id,
        "is_payment": False
    })

    return Locker(locker_number=id, is_avaliable=not (count > 0))


@app.get('/locker/payment/{nisit_id}')
def show_payment(nisit_id: str):
    doc = collection.find_one({"nisit_id": nisit_id, "is_payment": False},
                              {"price": 1, "withdraw_date": 1})
    if doc['withdraw_date'] is None:
        raise HTTPException(400, {
            "error": "This transaction is not withdrawed"
        })

    return TotalPayment(nisit_id=doc['nisit_id'], total_payment=doc['price'])


@app.put('/locker/payment/{nisit_id}')
def pay_transaction(nisit_id: str, dto: Payment):
    order = collection.find_one({"nisit_id": nisit_id, "is_payment": False})

    if order['price'] > dto.price:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, {
            "error": "Money is not enough for paying this transaction"
        })

    collection.update_one(order, {"$set": {"is_payment": True}})
    return Receipt(
        nisit_id=nisit_id,
        total_payment=order['price'],
        cash=dto.price,
        change=dto.price - order['price']
    )


@app.put('/locker/withdraw/{nisit_id}')
def withdraw_item(nisit_id: str):
    order = collection.find_one({"nisit_id": nisit_id, "is_payment": False})
    actual_withdraw_time = datetime.now()
    total_payment = calculate_payment(
        order['expected_date'], order['initial_date']) + calculate_fee(order['expected_date'], actual_withdraw_time)
    # add fee

    collection.update_one(order, {"$set": {"withdraw_date": actual_withdraw_time,
                                  "price": total_payment}})

    return TotalPayment(nisit_id=nisit_id, total_payment=total_payment)
