from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.schemas.user import UserBase
from sqlalchemy import select



# --- CRUD Operations ---
def create_user(session: Session, user_in: UserBase):
    try:
        new_user = User(
            email=user_in.email,
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user

    except SQLAlchemyError as e:
        session.rollback()
        # logger.exception("Database error during product creation")
        raise


def get_user_by_email(session: Session, email: str) :
    try:
        user = session.query(User).filter(User.email == email).first()
        if not user:
           return None

        return user

    except SQLAlchemyError as e:
        session.rollback()
        # logger.exception("Database error during get_product_by_id")
        return None
