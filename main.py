from fastapi import FastAPI, Depends, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from database import get_db, engine, Base
import schemas
import user_service

app = FastAPI()

Base.metadata.create_all(bind=engine)

def build_response(status_code: int, message: str, path: str, data: any = None, error: str = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "message": message,
            "error": error,
            "data": data,
            "path": path,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    )

@app.post("/menu-items", status_code=status.HTTP_201_CREATED)
def create_menu_item(request: Request, payload: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    existing_item = user_service.get_by_dish_code(db, payload.dish_code)
    if existing_item:
        return build_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Mã món ăn (dish_code) đã tồn tại trên hệ thống",
            error="Bad Request",
            path=str(request.url.path)
        )
    try:
        new_item = user_service.create(db, payload)
        data_res = schemas.MenuItemResponseData.model_validate(new_item).model_dump()
        return build_response(
            status_code=status.HTTP_201_CREATED, 
            message="Thêm món ăn mới thành công", 
            data=data_res, 
            path=str(request.url.path)
        )
    except Exception as e:
        return build_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            message="Lỗi hệ thống khi thêm món ăn", 
            error=str(e), 
            path=str(request.url.path)
        )

@app.get("/menu-items")
def get_all_menu_items(request: Request, db: Session = Depends(get_db)):
    items = user_service.get_all(db)
    data_res = [schemas.MenuItemResponseData.model_validate(item).model_dump() for item in items]
    return build_response(
        status_code=status.HTTP_200_OK, 
        message="Lấy danh sách món ăn thành công", 
        data=data_res, 
        path=str(request.url.path)
    )

@app.get("/menu-items/{item_id}")
def get_menu_item_detail(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = user_service.get_by_id(db, item_id)
    if not item:
        return build_response(
            status_code=status.HTTP_404_NOT_FOUND, 
            message="Menu item not found", 
            error="Not Found", 
            path=str(request.url.path)
        )
    data_res = schemas.MenuItemResponseData.model_validate(item).model_dump()
    return build_response(
        status_code=status.HTTP_200_OK, 
        message="Lấy thông tin món ăn thành công", 
        data=data_res, 
        path=str(request.url.path)
    )

@app.put("/menu-items/{item_id}")
def update_menu_item(item_id: int, request: Request, payload: schemas.MenuItemUpdate, db: Session = Depends(get_db)):
    item = user_service.get_by_id(db, item_id)
    if not item:
        return build_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Menu item not found", 
            error="Not Found", 
            path=str(request.url.path)
        )
    try:
        if payload.dish_code:
            existing_code = user_service.get_by_dish_code(db, payload.dish_code)
            if existing_code and existing_code.id != item_id:
                return build_response(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    message="Mã món ăn (dish_code) đã tồn tại ở một món ăn khác", 
                    error="Bad Request", 
                    path=str(request.url.path)
                )
        
        updated_item = user_service.update(db, item, payload)
        data_res = schemas.MenuItemResponseData.model_validate(updated_item).model_dump()
        return build_response(
            status_code=status.HTTP_200_OK, 
            message="Cập nhật món ăn thành công", 
            data=data_res, 
            path=str(request.url.path)
        )
    except Exception as e:
        return build_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            message="Lỗi hệ thống khi cập nhật món ăn", 
            error=str(e), path=str(request.url.path)
        )

@app.delete("/menu-items/{item_id}")
def delete_menu_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = user_service.get_by_id(db, item_id)
    if not item:
        return build_response(
            status_code=status.HTTP_404_NOT_FOUND, 
            message="Menu item not found", 
            error="Not Found", 
            path=str(request.url.path)
        )
    try:
        user_service.delete(db, item)
        return build_response(
            status_code=status.HTTP_200_OK, 
            message="Xóa món ăn thành công", 
            data=None, 
            path=str(request.url.path)
        )
    except Exception as e:
        return build_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            message="Lỗi hệ thống khi xóa món ăn", 
            error=str(e), 
            path=str(request.url.path)
        )
