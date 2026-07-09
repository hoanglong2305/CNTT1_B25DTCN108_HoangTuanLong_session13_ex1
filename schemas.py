from pydantic import BaseModel, Field
from typing import Any, Optional, Literal
from datetime import datetime

class MenuItemBase(BaseModel):
    dish_code: str = Field(..., max_length=50, description="Mã món ăn duy nhất")
    dish_name: str = Field(..., min_length=1, description="Tên món ăn không được rỗng")
    calorie_count: int = Field(..., gt=0, description="Hàm lượng calo phải lớn hơn 0")
    price: float = Field(..., gt=0, description="Đơn giá phải lớn hơn 0")
    status: Literal["AVAILABLE", "OUT_OF_STOCK"] = Field(default="AVAILABLE")

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    dish_code: Optional[str] = Field(None, max_length=50)
    dish_name: Optional[str] = Field(None, min_length=1)
    calorie_count: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["AVAILABLE", "OUT_OF_STOCK"]] = None

class MenuItemResponseData(BaseModel):
    id: int
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str

    class Config:
        from_attributes = True