from fastapi import APIRouter, HTTPException, Form, status, Request, Response, Depends
from sqlmodel import Session, select
from models import Customer
from database import engine
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.future import select

router = APIRouter()
templates = Jinja2Templates(directory="templates")
session = Session(bind=engine)


@router.get('/profile/{cust_id}', response_model=Customer)
async def get_profile(request: Request, cust_id: int):
    statement = select(Customer).where(Customer.id == cust_id)
    result = session.exec(statement).first()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "id": result.id,
        "first_name": result.first_name,
        "second_name": result.second_name,
        "phone": result.phone,
        "email": result.email,
        "address": result.address
    })


@router.post('/registration', status_code=status.HTTP_201_CREATED)
async def create_a_customer(
        first_name: str = Form(...),
        second_name: str = Form(...),
        email: str = Form(...),
        address: str = Form(...),
        phone: int = Form(...),
        password: str = Form(...),
        remember: bool = Form(default=False)
) -> RedirectResponse:
    statement = select(Customer).where((Customer.email == email) | (Customer.phone == phone))
    result = session.exec(statement).one_or_none()

    if result is None:
        new_cust = Customer(
            first_name=first_name,
            second_name=second_name,
            phone=phone,
            email=email,
            password=password,
            address=address
        )
        session.add(new_cust)
        session.commit()

        # Перенаправление на страницу профиля после успешной регистрации
        response = RedirectResponse(url=f"/user/profile/{new_cust.id}", status_code=302)
        if remember:
            response.set_cookie(key="id", value=str(new_cust.id), max_age=15695000)
        return response

    # Вывод ошибки, если пользователь уже существует
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer already exists")


@router.post('/login')
async def get_cust(email_login: str = Form(...), password_login: str = Form(...),
                   remember: bool = Form(default=False)) -> Response:
    email_statement = select(Customer).where(Customer.email == email_login)
    email_result = session.exec(email_statement).first()
    password_statement = select(Customer).where(Customer.password == password_login)
    password_result = session.exec(password_statement).first()

    if email_result and email_result.id == password_result.id:
        response = RedirectResponse(url=f"/user/profile/{email_result.id}", status_code=302)
        if remember:
            response.set_cookie(key="id", value=str(email_result.id), max_age=15695000)
        return response

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@router.get('/login', tags=['Pages'])
async def get_login_page(request: Request):
    cookie = request.cookies.get('id')
    if cookie:
        return RedirectResponse(url=f"/user/profile/{cookie}")
    return templates.TemplateResponse("login.html", {"request": request})


@router.get('/registration', tags=['Pages'])
async def get_registration_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.delete('/profile/{cust_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_cust(cust_id: int):
    statement = select(Customer).where(Customer.id == cust_id)
    result = session.exec(statement).one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
    session.delete(result)
    session.commit()


@router.get('/profile', tags=['Account'])
async def switch_account(response: Response):
    response = RedirectResponse(url="/user/login")
    response.delete_cookie('id')
    return response


@router.get("/cart", tags=["Pages"])
async def get_cart_page(request: Request):
    user_id = request.cookies.get("id")
    if user_id is not None:
        user_id = int(user_id)
    else:
        user_id = None  # Если не авторизован, остается None

    return templates.TemplateResponse("cart.html", {"request": request, "user_id": user_id})


@router.get("/confirm_order", tags=["Order"])
async def confirm_order(request: Request, user_id: int = None):
    if user_id is None:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Необходима авторизация"})

    # Получаем информацию о пользователе из базы данных
    user = session.execute(select(Customer).where(Customer.id == user_id)).scalars().first()
    if not user:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Пользователь не найден"})

    return templates.TemplateResponse("payment.html", {"request": request, "address": user.address})
