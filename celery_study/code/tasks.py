# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery_study.code.celery import app


@app.task()
def hello2():
    return "hello world drop"
