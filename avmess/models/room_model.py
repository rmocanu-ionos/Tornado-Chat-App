from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from avmess.models.user_model import UserModel
from avmess.server_utils import ROOMS


class RoomModel(models.Model):

    class Meta:
        db_table = "roommodel"

    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name_room', max_length=50)
    topic = models.CharField(db_column='topic_room', max_length=50)

    def add_entry(self, name, topic):
        self.name = name
        self.topic = topic

    def __str__(self):
        return "{}  {} {}".format(self.id, self.name, self.topic)

    @classmethod
    def get_users(cls, room_id):
        info = []

        try:
            room = RoomModel.objects.get(id=room_id)

        except ObjectDoesNotExist:
            return {'error': 'Room does not exist'}

        for user_id in ROOMS[room.id]:
            user = UserModel.objects.get(id=user_id)
            info.append(user.serialize())

        return info

    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'topic': self.topic
        }
