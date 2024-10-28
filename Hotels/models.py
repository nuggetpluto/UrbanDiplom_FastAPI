from typing import Optional
from sqlmodel import SQLModel, Field


class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    second_name: str
    phone: str  # Используйте str для номера телефона, чтобы избежать проблем с ведущими нулями
    email: str
    password: str
    address: str


class Hotel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    price: float  # Изменено на float для более точной цены


class Cart(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hotel_id: int


