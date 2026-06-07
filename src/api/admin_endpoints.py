from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.roles import RoleRequestAdd

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/roles")
async def create_roles(
        db: DBDep,
        role_data: RoleRequestAdd,
):
    role = await db.roles.add(role_data)
    await db.commit()

    return {"status": "OK", "role": role}