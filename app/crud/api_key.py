from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.models.api_key import APIKey
from app.schemas.api_key import APIKeyResponse
from pydantic import Field
from app.crud.helper import ResponseModel, success_response,error_response
from sqlalchemy import select
from app.crud.user import get_user_by_email
import secrets


def generate_api_key(length: int = 32) -> str:
    # Generates a URL-safe text string, e.g., for API keys or tokens
    return "Dk_"+ secrets.token_urlsafe(length)


def create_api_key(session:Session, user_id:str):
    try:
        user = get_user_by_email(session, user_id)
        if user is not None:
            new_key = generate_api_key()

            new_key = APIKey(
                key =  new_key,
                user_id = user.email
            )

            session.add(new_key)
            session.commit()
            session.refresh(new_key)

            return new_key
        else:
            return None
    except SQLAlchemyError as e:
        session.rollback()
        # logger.exception("Database error during product creation")
        raise









