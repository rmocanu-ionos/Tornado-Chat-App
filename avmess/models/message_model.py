from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from avmess.models.user_model import UserModel
from avmess.models.room_model import RoomModel


class MessageModel(models.Model):

    class Meta:
        db_table = "messagemodel"

    id = models.AutoField(db_column='id', primary_key=True)
    user_id = models.ForeignKey(UserModel, on_delete=models.SET_NULL)
    room_id = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    data = models.CharField(db_column='message_data', max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_entry(self, user, room, data):
        self.user_id = user
        self.room_id = room
        self.data = data

    def __str__(self):
        return "{}  {} {} {} {}".format(self.id, self.user_id, self.room_id, self.data, self.created_at)

    def serialize(self):

        return {
            'id': self.id,
            'user_id': self.user_id.id,
            'room_id': self.room_id.id,
            'data': self.data,
            'created_at': self.created_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
