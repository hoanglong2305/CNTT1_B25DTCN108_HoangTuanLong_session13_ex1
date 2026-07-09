from sqlalchemy.orm import Session
import models
import schemas

def get_by_id(db: Session, item_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()

def get_by_dish_code(db: Session, dish_code: str):
    return db.query(models.MenuItem).filter(models.MenuItem.dish_code == dish_code).first()

def get_all(db: Session):
    return db.query(models.MenuItem).all()

def create(db: Session, payload: schemas.MenuItemCreate):
    try:
        new_item = models.MenuItem(**payload.model_dump())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        db.rollback()
        raise e

def update(db: Session, item: models.MenuItem, payload: schemas.MenuItemUpdate):
    try:
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
        return item
    except Exception as e:
        db.rollback()
        raise e

def delete(db: Session, item: models.MenuItem):
    try:
        db.delete(item)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
