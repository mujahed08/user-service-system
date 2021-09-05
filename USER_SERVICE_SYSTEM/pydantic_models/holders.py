from typing import List
from pydantic import BaseModel

from USER_SERVICE_SYSTEM.domain.models import UserIn_Pydantic

class RoleOps(BaseModel):
    id:int
    name:str

class UserRoleOps(BaseModel):
    user:UserIn_Pydantic
    roles:List[RoleOps]
