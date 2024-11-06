from sqlmodel import Session, select
from models import Customer


def get_customer_by_id(session: Session, cust_id: int):
    statement = select(Customer).where(Customer.id == cust_id)
    return session.exec(statement).first()


def create_customer(session: Session, first_name: str, second_name: str, email: str, address: str, phone: str,
                    password: str):
    existing_customer = select(Customer).where(Customer.email == email or Customer.phone == phone)
    if session.exec(existing_customer).first():
        return None
    new_customer = Customer(first_name=first_name, second_name=second_name, email=email, address=address, phone=phone,
                            password=password)
    session.add(new_customer)
    session.commit()
    return new_customer


def delete_customer(session: Session, cust_id: int):
    customer = get_customer_by_id(session, cust_id)
    if customer:
        session.delete(customer)
        session.commit()
        return True
    return False


