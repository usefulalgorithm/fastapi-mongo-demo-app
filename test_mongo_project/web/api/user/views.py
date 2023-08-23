from typing import Optional

from fastapi import APIRouter, HTTPException, status

from test_mongo_project.db.models.user_model import UserModel
from test_mongo_project.web.api.user.schema import UpdatePassword, UserCreate, UserView

router = APIRouter()


@router.get("/", response_model=list[UserView])
async def read_users(skip: int = 0, limit: int = 100) -> list[UserModel]:
    return await UserModel.find_all(skip=skip, limit=limit).to_list()


@router.post("/", response_model=UserView)
async def create_user(user_create: UserCreate) -> UserModel:
    model = UserModel(**user_create.model_dump(by_alias=True))
    await UserModel.insert_one(model)
    return model


@router.get("/{user_id}", response_model=UserView)
async def read_user_by_id(user_id: str) -> UserModel:
    res = await UserModel.get(user_id)
    if not res:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"No user found with id = {user_id}",
        )
    return res


@router.put("/{user_id}/password")
async def update_user_password(user_id: str, update_password: UpdatePassword) -> None:
    model = await UserModel.get(user_id)
    if not model:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"No user found with id = {user_id}",
        )
    await model.update({"$set": update_password.model_dump(by_alias=True)})


@router.delete("/{user_id}", response_model=Optional[UserView])
async def delete_user_by_id(user_id: str) -> Optional[UserModel]:
    model = await UserModel.get(user_id)
    if model is not None:
        await model.delete()
    return model
