from fastapi import FastAPI
from models import Customer

app = FastAPI(title="My API", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "Hello world"}
    
@app.post("/customers")
async def create_customer(customer: Customer):
    return Customer