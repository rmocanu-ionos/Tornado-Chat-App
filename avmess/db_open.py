import os
import sys

sys.path.insert(0, os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avmess.django_settings")

from django import db, setup

setup()

from avmess.models.user_model import UserModel
from avmess.models.message_model import MessageModel
from avmess.models.room_model import RoomModel


with db.connection.schema_editor() as schema_editor:
    schema_editor.create_model(UserModel)
    schema_editor.create_model(RoomModel)
    schema_editor.create_model(MessageModel)
