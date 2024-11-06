from sqlmodel import Session, select
from models import Hotel, Cart


def get_all_hotels(session: Session, title: str = None, min_price: float = None, max_price: float = None):
    statement = select(Hotel)
    if title:
        statement = statement.where(Hotel.title.contains(title))
    if min_price:
        statement = statement.where(Hotel.price >= min_price)
    if max_price:
        statement = statement.where(Hotel.price <= max_price)
    return session.exec(statement).all()


def get_hotel_by_id(session: Session, hotel_id: int):
    statement = select(Hotel).where(Hotel.id == hotel_id)
    return session.exec(statement).first()


def create_hotel(session: Session, hotel: Hotel):
    session.add(hotel)
    session.commit()
    return hotel


def update_hotel(session: Session, hotel_id: int, hotel: Hotel):
    existing_hotel = get_hotel_by_id(session, hotel_id)
    if existing_hotel:
        existing_hotel.title = hotel.title
        existing_hotel.price = hotel.price
        session.commit()
    return existing_hotel


def delete_hotel(session: Session, hotel_id: int):
    hotel = get_hotel_by_id(session, hotel_id)
    if hotel:
        session.delete(hotel)
        session.commit()


def add_to_cart(session: Session, hotel_id: int):
    statement = select(Hotel).where(Hotel.id == hotel_id)
    hotel = session.exec(statement).first()
    if not hotel:
        return None
    new_cart_item = Cart(hotel_id=hotel.id)
    session.add(new_cart_item)
    session.commit()
    return new_cart_item
