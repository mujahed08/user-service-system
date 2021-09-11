"""
Tortoise ORM FastAPI
"""

import os
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from USER_SERVICE_SYSTEM.domain.models import RoleIn_Pydantic, RoleSer_Pydantic, Role_Pydantic, Role
from USER_SERVICE_SYSTEM.domain.models import UserIn_Pydantic, User_Pydantic, User, UserUp_Pydantic
from USER_SERVICE_SYSTEM.commons.logger import get_logger
from USER_SERVICE_SYSTEM.pydantic_models.enviornment import Settings
from USER_SERVICE_SYSTEM.pydantic_models.holders import UserRoleOps

run_env:str = os.environ['RUN_ENV']
settings = Settings(_env_file=f'{run_env}.env', _env_file_encoding='utf-8')

logger = get_logger('main.py')

logger.info('   Initiliazing Fast API app with Tortoise ORM  support')
app = FastAPI(title="Tortoise ORM FastAPI")
logger.info('   Initialized Fast API app')

logger.info('   Registring Tortoise ORM with Fast API app')

register_tortoise(
    app,
    db_url=f'mysql://root:{settings.mysql_root_password}@{settings.mysql_host}:3306/{settings.mysql_database}',
    modules={"models": ["USER_SERVICE_SYSTEM.domain.models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)

class Status(BaseModel):
    message: str


@app.get("/user-service-system/users", response_model=List[User_Pydantic])
async def get_users():
    logger.info('   get_users function is executing')
    return await User_Pydantic.from_queryset(User.all())


@app.post("/user-service-system/users", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    logger.info(user)
    logger.info('   create_user function is executing')
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@app.get("/user-service-system/users/{user_id}", response_model=User_Pydantic,
responses={404: {"model": HTTPNotFoundError}})
async def get_user(user_id: int):
    logger.info('   get_user function is executing')
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@app.put("/user-service-system/users/{user_id}", response_model=User_Pydantic,
responses={404: {"model": HTTPNotFoundError}})
async def update_user(user_id: int, user: UserUp_Pydantic):
    logger.info('<<< update_user function is executing >>>')
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


@app.delete("/user-service-system/users/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int):
    logger.info('   delete_user function is executing')
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    logger.info('   deleted_count: %d', deleted_count)
    return Status(message=f'Deleted user {user_id}')

@app.post("/user-service-system/roles", response_model=Role_Pydantic)
async def create_role(role_py: Role_Pydantic):
    logger.info('   create_role function is executing')
    role = await Role.create(**role_py.dict(exclude_unset=True))
    return await Role_Pydantic.from_tortoise_orm(role)

@app.put("/user-service-system/roles/{role_id}", response_model=Role_Pydantic,
responses={404: {"model": HTTPNotFoundError}})
async def update_role(role_id: int, role_py: RoleIn_Pydantic):
    logger.info('   update_role function is executing')
    await Role.filter(id=role_id).update(**role_py.dict(exclude_unset=True))
    return await Role_Pydantic.from_queryset_single(Role.get(id=role_id))

@app.delete("/user-service-system/roles/{role_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_role(role_id: int):
    logger.info('   delete_role function is executing')
    deleted_count = await Role.filter(id=role_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {role_id} not found")
    logger.info('   deleted_count: %d', deleted_count)
    return Status(message=f'Deleted user {role_id}')

@app.post("/user-service-system/users/{user_id}/roles", response_model=Status)
async def assign_roles(user_id:int, names: List[str]):
    logger.info('   assign_roles function is executing')
    logger.info(names)
    roles = await Role.filter(name__in=names).all()
    logger.info(roles)
    user = await User.get(id=user_id)
    await user.roles.add(*roles)
    logger.info('   roles added')
    return Status(message=f'Added roles {names} to user {user.username}')

@app.delete("/user-service-system/users/{user_id}/roles", response_model=Status)
async def remove_roles(user_id: int, names: List[str]):
    logger.info('   remove_roles function is executing')
    logger.info(names)
    roles_to_remove = await Role.filter(name__in=names).all()
    user = await User.get(id=user_id)
    await user.roles.remove(*roles_to_remove)
    logger.info('   roles removed %s', names)
    return Status(message=f'Removed roles {names} from user {user.username}')

@app.post("/user-service-system/roles/ops", response_model=User_Pydantic,
responses={404: {"model": HTTPNotFoundError}})
async def roles_ops(user_role:UserRoleOps):
    logger.info('   roles_ops function is executing')
    logger.info(user_role.json())
    logger.info('   ')
    roles = await RoleSer_Pydantic.from_queryset(Role.filter(id__in=[1,99]))
    logger.info('   query for id__in=[1,99]')
    logger.info(roles[0].json())
    logger.info('   ')
    role = await Role.get(name='ROLE_SA')
    logger.info('   > Role.get(name=\'ROLE_SA\')')
    user = await User.get(id=1)
    logger.info('   > user = await User.get(id=1)')
    await user.roles.add(role)
    logger.info('   > user.roles.remove(role)')
    logger.info('   >')
    return await User_Pydantic.from_queryset_single(User.get(id=1))

logger.info('   End of the main file')
