from fastapi import APIRouter # type: ignore
from fastapi import Depends # type: ignore
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.product import create_product,get_product_by_id,get_all_products,delete_product, update_product
from app.schemas.product import ProductCreate,ProductOut
from app.api.deps import get_api_key
from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

product_router = APIRouter(prefix="/products", tags=["Product"])

@product_router.get('/',dependencies=[Depends(get_api_key)])
async def Get_AllProduct(db: Session = Depends(get_db)):
    retrive_products = get_all_products(db)
    return {"products": retrive_products.data}

@product_router.get('/{id}',dependencies=[Depends(get_api_key)])
async def Get_product(id:int ,db: Session = Depends(get_db)):
    retrive_product = get_product_by_id(db,id)
    if retrive_product.data is not None:
        return {"product": retrive_product.data}  # Return the single product as response
    else:
        return {"message": "Product not found"}

@product_router.post('/{id}',dependencies=[Depends(get_api_key)])
async def Add_product(id:int,product_in: ProductCreate ,db: Session = Depends(get_db)):
    new_product  = create_product(db, product_in)
    if new_product.data is not None:
        return {"product": new_product.data}  # Return the created product
    else:
        return {"message": "Failed to create product"}
    
@product_router.delete('/{id}',dependencies=[Depends(get_api_key)])
async def Delete_product(id:int, db:Session = Depends(get_db)):
    deleted_product = delete_product(db,id)
    if deleted_product.data is not None:
        return {"message": deleted_product.message}  # Return success message
    else:
        return {"message": "Product not found"}

@product_router.put('/{id}',dependencies=[Depends(get_api_key)])
async def update_product(id:int, db:Session = Depends(get_db),):
    updated_product = update_product(db,id)
    if updated_product.data is not None:
        return {"message": updated_product.message}  # Return success message
    else:
        return {"message": "Product not found"}

