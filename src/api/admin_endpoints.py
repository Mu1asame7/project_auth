from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.roles import RoleRequestAdd
from src.utils.decorator_roles import RolesChecker

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/roles")
@RolesChecker(["Admin"])
async def create_roles(
        db: DBDep,
        user_id: UserIdDep,
        role_data: RoleRequestAdd,
):
    role = await db.roles.add(role_data)
    await db.commit()

    return {"status": "OK", "role": role}