# from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from apps.accounts.views import SignUpView
# obj = SignUpView()
# user_id = obj.object.id

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("config.settings", namespace="CELERY")

app.autodiscover_tasks()

# app.config.beat_schedule = {
#     'delete-user-after-3-day': {
#         'task': 'apps.accounts.tasks.delete_user',
#         'schedule': 60,
#         'args': (user_id,)
#     },
# }
# app.conf.timezone = 'UTC'
