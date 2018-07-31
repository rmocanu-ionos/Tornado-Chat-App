import os
import sys
sys.path.insert(0, os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "avmess.django_settings")

from django import db, setup
setup()

from avmess.models.user_model import UserModel
from avmess.models.room_model import RoomModel
from avmess.models.message_model import MessageModel

# with db.connection.schema_editor() as schema_editor:
#     schema_editor.delete_model(MessageModel)
#     schema_editor.delete_model(UserModel)
#     schema_editor.delete_model(RoomModel)


with db.connection.schema_editor() as schema_editor:
    schema_editor.create_model(UserModel)
    schema_editor.create_model(RoomModel)
    schema_editor.create_model(MessageModel)

t = UserModel()
t.add_entry('daniel', 'radu')
t.save()

for i in UserModel.objects.all():
    print(i)

t = RoomModel()
t.add_entry('Project', 'About AvMess')
t.save()

t = MessageModel()
t.add_entry(UserModel.objects.get(id=1), RoomModel.objects.get(id=1), 'First message')
t.save()

assert t.id is not None

print(MessageModel.objects.get(user_id=UserModel.objects.get(id=1)))

with db.connection.schema_editor() as schema_editor:
    schema_editor.delete_model(MessageModel)
    schema_editor.delete_model(UserModel)
    schema_editor.delete_model(RoomModel)

