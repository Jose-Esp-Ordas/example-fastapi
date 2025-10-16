from fastapi import FastAPI, Query, Depends, HTTPException
from models import Customer
from sqlmodel import Field, Session, create_engine, select, SQLModel
from esquemas import CustomerCreate, CustomerRead
import os
from typing import Annotated
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="My API", version="0.1.0")
target_metadata = SQLModel.metadata


engine = create_engine(os.getenv("DATABASE_URL"))

lista_usuarios = []

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/")
async def root():
    return {"message": "Hello world"}
    
@app.post("/customers", response_model=CustomerRead)
def create_customer(customer_data: CustomerCreate, session: SessionDep):
    # Verificar si ya existe email o teléfono
    existing = session.exec(
        select(Customer).where(
            (Customer.email == customer_data.email) |
            (Customer.phone == customer_data.phone)
        )
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email o teléfono ya existen")

    new_customer = Customer(**customer_data.model_dump())
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return new_customer

# 📌 Listar clientes
@app.get("/customers", response_model=list[CustomerRead])
def list_customers(session: SessionDep):
    customers = session.exec(select(Customer)).all()
    if not customers:
        raise HTTPException(status_code=404, detail="No existen usuarios registrados")
    return customers