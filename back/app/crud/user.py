from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from app import schemas
from app.core.security import get_password_hash
from app.crud._base import CRUDBase
from app.models.user import User


class CRUDUser(CRUDBase[User, schemas.UserCreate, schemas.UserUpdate]):
    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: schemas.UserCreate) -> User:
        create_data = obj_in.model_dump()
        create_data.pop("password")
        db_obj = User(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()

        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: Union[schemas.UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db=db, db_obj=db_obj, obj_in=update_data)


user = CRUDUser(User)
