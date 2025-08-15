from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.models.order import Order
from app.models.product import Product
from app.crud.product import get_product_by_id
from app.schemas.order import OrderCreate, OrderUpdate, OrderOut
from pydantic import Field
from app.crud.helper import ResponseModel, success_response,error_response


def create_order(session: Session, order_in: OrderCreate):
    try:
        product_response = get_product_by_id(session, order_in.product_id)
        if((product_response.success == True) and (product_response.data.stock >= order_in.quantity)):
            new_order = Order(
                product_id=order_in.product_id,
                quantity =order_in.quantity,
                status=order_in.status
            )
            session.add(new_order)
            
            product = session.query(Product).filter(Product.id == order_in.product_id).first()
             # Decrement stock
            product.stock -= order_in.quantity
            session.commit()
            session.refresh(new_order)
            return success_response("order created successfully", new_order)
        else:
            return error_response(f"Product is not available")

    except SQLAlchemyError as e:
        session.rollback()
        # logger.exception("Database error during product creation")
        return error_response(f"Database error: {str(e)}")


def get_order_by_id(session:Session, id: int)-> ResponseModel[OrderOut]:
    try:
        order = session.query(Order).filter(Order.id == id).first()
        if not order:
            return error_response("order not found")

        return success_response("order retrieved successfully", order)

    except SQLAlchemyError as e:
        # logger.exception("Database error during get_product_by_id")
        return error_response(f"Database error: {str(e)}")

def get_all_orders(session:Session)-> ResponseModel[List[OrderOut]]:
    try:
        order = session.query(Order).order_by(Order.id).all()
        return success_response(f"Retrieved {len(order)} orders", order)

    except SQLAlchemyError as e:
        # logger.exception("Database error during get_all_products")
        return error_response(f"Database error: {str(e)}")
    
def update_order(session, order_update: OrderUpdate, id: int):
    try:
        order_to_update = session.get(Order, id)
        if not order_to_update:
            return error_response("Order record not found")

        old_product = session.query(Product).filter(Product.id == order_to_update.product_id).first()
        new_product_id = order_update.product_id if order_update.product_id is not None else order_to_update.product_id
        new_quantity = order_update.quantity if order_update.quantity is not None else order_to_update.quantity

        new_product = session.query(Product).filter(Product.id == new_product_id).first()
        if not new_product:
            return error_response("New product not found")

        # Calculate stock adjustments
        if new_product_id == order_to_update.product_id:
            # Same product: check if stock can cover difference in quantity
            quantity_diff = new_quantity - order_to_update.quantity
            if quantity_diff > 0 and new_product.stock < quantity_diff:
                return error_response("Insufficient stock for the requested quantity")
            new_product.stock -= quantity_diff
        else:
            # Different product:
            # Return stock to old product
            old_product.stock += order_to_update.quantity
            # Check new product stock
            if new_product.stock < new_quantity:
                return error_response("Insufficient stock for the new product")
            new_product.stock -= new_quantity

        # Update order fields
        order_to_update.product_id = new_product_id
        order_to_update.quantity = new_quantity
        if order_update.status is not None:
            order_to_update.status = order_update.status

        session.commit()
        session.refresh(order_to_update)

        return success_response("Order updated successfully", order_to_update)

    except SQLAlchemyError as e:
        session.rollback()
        return error_response(f"Database error: {str(e)}")

def delete_order(session, id: int):
    try:
        order_to_delete = session.get(Order, id)
        if not order_to_delete:
            return error_response("order record not found")

        product = session.get(Product, order_to_delete.product_id)
        if not product:
            return error_response("Product record not found")
        
        # update stock in Product Table
        product.stock += order_to_delete.quantity
       
        # Now delete the order
        session.delete(order_to_delete)
        session.commit()

        return success_response("order record deleted successfully")

    except SQLAlchemyError as e:
        session.rollback()
        return error_response(f"Database error: {str(e)}")
