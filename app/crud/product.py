from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.crud.helper import ResponseModel, success_response,error_response
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from pydantic import Field
from pydantic.generics import GenericModel


# --- CRUD Operations ---
def create_product(session: Session, product_in: ProductCreate) -> ResponseModel[ProductOut]:
    try:
        new_product = Product(
            sku=product_in.sku,
            name=product_in.name,
            price=product_in.price,
            stock=product_in.stock
        )
        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        return success_response("Product created successfully", new_product)

    except SQLAlchemyError as e:
        session.rollback()
        # logger.exception("Database error during product creation")
        return error_response(f"Database error: {str(e)}")


def get_all_products(session: Session) -> ResponseModel[List[ProductOut]]:
    try:
        products = session.query(Product).order_by(Product.id).all()
        return success_response(f"Retrieved {len(products)} products", products)

    except SQLAlchemyError as e:
        session.rollback()
        # logger.exception("Database error during get_all_products")
        return error_response(f"Database error: {str(e)}")


def get_product_by_id(session: Session, id: int) -> ResponseModel[ProductOut]:
    try:
        product = session.get(Product, id)
        if not product:
            return error_response("Product not found")

        return success_response("Product retrieved successfully", product)

    except SQLAlchemyError as e:
        session.rollback()
        # logger.exception("Database error during get_product_by_id")
        return error_response(f"Database error: {str(e)}")


def delete_product(session: Session, id: int) -> ResponseModel[None]:
    try:
        product_to_delete = session.get(Product, id)
        if not product_to_delete:
            return error_response("Product record not found")

        session.delete(product_to_delete)
        session.commit()
        return success_response("Product record deleted successfully")

    except SQLAlchemyError as e:
        session.rollback()
        # logger.exception("Database error during delete_product")
        return error_response(f"Database error: {str(e)}")


def update_product(session: Session, product_update: ProductUpdate, id: int) -> ResponseModel[ProductOut]:
    try:
        product_to_update = session.get(Product, id)
        if not product_to_update:
            return error_response("Product record not found")

        if product_update.name is not None:
            product_to_update.name = product_update.name
        if product_update.price is not None:
            product_to_update.price = product_update.price
        if product_update.sku is not None:
            product_to_update.sku = product_update.sku
        if product_update.stock is not None:
            product_to_update.stock = product_update.stock

        session.commit()
        session.refresh(product_to_update)

        return success_response("Product record updated successfully", product_to_update)

    except SQLAlchemyError as e:
        session.rollback()
        # logger.exception("Database error during update_product")
        return error_response(f"Database error: {str(e)}")