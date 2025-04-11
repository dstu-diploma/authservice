from tortoise.models import Model
from tortoise import fields


class UserTokensModel(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField()
    token_revision = fields.IntField(default=0)

    def verify_revision(self, rev: int):
        return self.token_revision == rev

    def increase_revision(self):
        self.token_revision += 1
        self.save(update_fields=("token_revision",))

    class Meta:
        table: str = "usertokens"
