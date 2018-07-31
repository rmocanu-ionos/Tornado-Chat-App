from django.db import models


class UserModel(models.Model):

    class Meta:
        db_table = "usermodel"

    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name_user', max_length=50)
    password = models.CharField(db_column='password_user', max_length=100)

    def add_entry(self, name, passwd):
        self.name = name
        self.password = passwd

    def __str__(self):
        return "{}  {} {}".format(self.id, self.name, self.password)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }
