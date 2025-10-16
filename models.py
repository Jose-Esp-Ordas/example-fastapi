from sqlmodel import SQLModel, Field

class Customer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(index=True, unique=True)
    phone: str | None = Field(index=True, unique=True)
    address: str | None = Field(index=True)
