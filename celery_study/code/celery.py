# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from celery import Celery
# app = Celery()
app = Celery("zrg2017031201",
             broker="amqp://guest:guest@localhost:5672//",
             backend="redis://localhost:6379/0")

# app.config_from_object("celery_study.code.config")
# app.conf.result_expires = 10000
app.conf["CELERY_TASK_RESULT_EXPIRES"] = 100

@app.task
def hello1():
    return 1+2
