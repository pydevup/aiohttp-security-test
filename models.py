from tortoise import Model, fields


class Users(Model):
    id = fields.IntField(pk=True, )
    login = fields.CharField(max_length=256, unique=True)
    passwd = fields.CharField(max_length=256, )
    is_superuser = fields.BooleanField(default=False, )
    disabled = fields.BooleanField(default=False, )


class Permissions(Model):
    id = fields.IntField(pk=True, )
    user = fields.ForeignKeyField(
        "models.Users",
        related_name="permissions",
        on_delete=fields.CASCADE,
    )
    perm_name = fields.CharField(max_length=64, )
