from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

myapp = FastAPI()

class Holding(BaseModel):
    name: str
    amount: float

class Portfolio(BaseModel):
    total: float
    holdings: List[Holding]

@myapp.post("/calculate")
def calculate_allocation(portfolio: Portfolio):
    allocations = [
        {"name": holding.name, "percentage": (holding.amount / portfolio.total) * 100}
        for holding in portfolio.holdings
    ]
    return {"allocations": allocations}