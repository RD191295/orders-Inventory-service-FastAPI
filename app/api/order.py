from fastapi import APIRouter
from fastapi import Depends # type: ignore
from app.api.deps import get_db
from sqlalchemy.orm import Session
from app.crud.order import create_order,get_all_orders,get_order_by_id,delete_order,update_order
from app.schemas.order import OrderCreate,OrderUpdate
from sqlalchemy.orm import Session
from app.api.deps import get_api_key


order_router = APIRouter(prefix="/order", tags=["Order"])


@order_router.get("/", dependencies=[Depends(get_api_key)])
async def Get_AllOrders(db: Session = Depends(get_db)):
    all_orders = get_all_orders(db)
    return {"orders": all_orders.data}

@order_router.get("/{id}",dependencies=[Depends(get_api_key)])
async def Get_Order(id:int,db: Session = Depends(get_db)):
    retrive_order = get_order_by_id(db,id)
    if retrive_order.data is not None:
        return {"order": retrive_order.data}  # Return the single product as response
    else:
        return {"message": "order not found"}

@order_router.put("/{id}",dependencies=[Depends(get_api_key)])
async def Update_order(id:int,order_update: OrderUpdate,db: Session = Depends(get_db)):
    order_update = update_order(db, order_update, id)
    if order_update.data is not None:
        return {"Updated Order":order_update.data}
    else:
        return {"message":order_update.message}

@order_router.delete("/{id}",dependencies=[Depends(get_api_key)])
async def Delete_order(id:int,db: Session = Depends(get_db)):
    deleted_order = delete_order(db,id)
    return {"message":deleted_order.message}

@order_router.post("/",dependencies=[Depends(get_api_key)])
async def Create_order(order_in: OrderCreate,db: Session = Depends(get_db)):
    created_order = create_order(db, order_in)
    if created_order.data is not None:
        return {"order": created_order.data}
    else:
        return {"message":created_order.message}