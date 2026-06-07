from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.roles import RoleRequestAdd, RoleUpdate, UserRoleAdd
from src.utils.decorator_roles import RolesChecker

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/roles")
@RolesChecker(["admin"])
async def get_roles(
        db: DBDep,
        user_id: UserIdDep,
):
    return await db.roles.get_all()


@router.post("/roles")
@RolesChecker(["admin"])
async def create_roles(
        db: DBDep,
        user_id: UserIdDep,
        role_data: RoleRequestAdd,
):
    role = await db.roles.add(role_data)
    await db.commit()

    return {"status": "OK", "role": role}


@router.patch("/roles/{role_id}")
@RolesChecker(["admin"])
async def update_role(
        role_id: int,
        db: DBDep,
        user_id: UserIdDep,
        role_data: RoleUpdate,
):
    await db.roles.edit(role_data, is_patch=True, id=role_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/roles/{role_id}")
@RolesChecker(["admin"])
async def delete_role(
        role_id: int,
        db: DBDep,
        user_id: UserIdDep,
):
    await db.roles.delete(id=role_id)
    await db.commit()
    return {"status": "OK"}


@router.get("/users/{target_user_id}/roles")
@RolesChecker(["admin"])
async def get_user_roles(
        target_user_id: int,
        db: DBDep,
        user_id: UserIdDep,
):
    roles = await db.user_roles.get_roles_by_user_id(target_user_id)
    return roles


@router.post("/users/{target_user_id}/roles")
@RolesChecker(["admin"])
async def assign_role_to_user(
        target_user_id: int,
        db: DBDep,
        user_id: UserIdDep,
        role_data: UserRoleAdd,
):
    role = await db.roles.get_one_or_none(id=role_data.role_id)
    print(role)
    if not role:
        raise HTTPException(status_code=404, detail="Роль не найдена")

    existing = await db.user_roles.get_one_or_none(user_id=target_user_id, role_id=role_data.role_id)
    print(existing)
    if existing:
        raise HTTPException(status_code=400, detail=f"У пользователя есть роль: {role_data.role_id}")

    await db.user_roles.add(role_data)
    await db.commit()

    return {"status": "OK"}


@router.delete("/users/{target_user_id}/roles/{role_id}")
@RolesChecker(["admin"])
async def remove_role_from_user(
        target_user_id: int,
        role_id: int,
        db: DBDep,
        user_id: UserIdDep,
):
    await db.user_roles.delete(user_id=target_user_id, role_id=role_id)
    await db.commit()
    return {"status": "OK"}