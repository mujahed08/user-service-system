from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=16)

    def __str__(self):
        return str(self.name)

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    username = fields.CharField(max_length=64)
    password = fields.CharField(max_length=256)
    enabled = fields.BooleanField(default=True)
    roles: fields.ManyToManyRelation['Role'] = fields.ManyToManyField('models.Role',
        through='user_role')

    def __str__(self):
        return str(self.name)

Role_Pydantic = pydantic_model_creator(Role, name="Role")
RoleSer_Pydantic = pydantic_model_creator(Role, name="RoleSer", include=['id', 'name'])
RoleIn_Pydantic = pydantic_model_creator(Role, name="RoleIn", exclude_readonly=True)
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
User_Pydantic = pydantic_model_creator(User, name="User", exclude=['password'])
UserUp_Pydantic = pydantic_model_creator(User, name="UserUp", exclude=['password', 'username'],
    exclude_readonly=True)
