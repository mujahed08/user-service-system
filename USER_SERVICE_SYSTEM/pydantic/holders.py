from typing import List
from pydantic import BaseModel

from USER_SERVICE_SYSTEM.domain.models import RoleIn_Pydantic, UserIn_Pydantic

"""
class User_Role(BaseModel):
    user_id: int
    role:str

"""

class RoleOps(BaseModel):
    id:int
    name:str

class UserRoleOps(BaseModel):
    user:UserIn_Pydantic
    roles:List[RoleOps]
