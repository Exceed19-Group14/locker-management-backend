from datetime import datetime
from fastapi import FastAPI
from database.db import collection
from dto import CreateLockerTransaction, LockerTransaction

app = FastAPI()


@app.post('/locker/deposit')
def deposit_item(dto: CreateLockerTransaction):
    doc = dto.dict()
    doc['initial_date'] = datetime.now()
    doc['withdraw_date'] = None
    
    
