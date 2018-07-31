from avmess.server_utils import ROOMS
from avmess.models.room_model import RoomModel


def rooms_setup():
    for room in RoomModel.objects.all():
        ROOMS[room.id] = set()