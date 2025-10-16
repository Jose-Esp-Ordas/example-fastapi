from pydantic import BaseModel, EmailStr
from typing import Optional

# Para crear un nuevo cliente
class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

# Para mostrar cliente (respuesta)
class CustomerRead(CustomerCreate):
    id: int

# Para actualización si luego quieres PATCH
class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
