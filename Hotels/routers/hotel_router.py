from fastapi import APIRouter, HTTPException, Form, status, Query, Request
from sqlmodel import Session, select
from models import Hotel, Cart
from database import engine
from fastapi.templating import Jinja2Templates
from collections import Counter

router = APIRouter()
templates = Jinja2Templates(directory="templates")
session = Session(bind=engine)


@router.get('/', name='get_all_hotel')
async def get_all_hotels(request: Request, title: str = Query(None), min_price: float = Query(None),
                         max_price: float = Query(None)):
    # Запрос для получения списка отелей
    statement = select(Hotel)
    if title:
        statement = statement.where(Hotel.title.contains(title))
    if min_price is not None:
        statement = statement.where(Hotel.price >= min_price)
    if max_price is not None:
        statement = statement.where(Hotel.price <= max_price)

    result = session.exec(statement).all()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # Получение уникальных цен и количества отелей для каждой цены
    all_prices = [hotel.price for hotel in result]
    price_count = Counter(all_prices)
    price_options = [{"price": price, "count": count} for price, count in sorted(price_count.items())]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result,
        "price_options": price_options
    })


@router.post('/cart/add', status_code=status.HTTP_201_CREATED)
async def add_to_cart(hotel_id: int = Form(...)):
    statement = select(Hotel).where(Hotel.id == hotel_id)
    hotel = session.exec(statement).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    new_cart_item = Cart(hotel_id=hotel.id)
    session.add(new_cart_item)
    session.commit()
    return {"detail": "Hotel added to cart"}


@router.get('/cart', tags=['Pages'])
async def get_cart_page_1(request: Request):
    statement = select(Cart)
    cart_items = session.exec(statement).all()
    return templates.TemplateResponse("cart.html", {"request": request, "cart_items": cart_items})


@router.post('/hotel', response_model=Hotel, status_code=status.HTTP_201_CREATED)
async def create_a_hotel(hotel: Hotel):
    session.add(hotel)
    session.commit()
    return hotel


@router.put('/hotel/{hotel_id}', response_model=Hotel)
async def update_a_hotel(hotel_id: int, hotel: Hotel):
    statement = select(Hotel).where(Hotel.id == hotel_id)
    existing_hotel = session.exec(statement).first()
    if not existing_hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    existing_hotel.title = hotel.title
    existing_hotel.price = hotel.price
    session.commit()
    return existing_hotel


@router.delete('/hotel/{hotel_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_hotel(hotel_id: int):
    statement = select(Hotel).where(Hotel.id == hotel_id)
    result = session.exec(statement).one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
    session.delete(result)
    session.commit()
