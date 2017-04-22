# -*- encoding: utf-8 -*-

CELERY_RESULT_BACKEND = u"redis://"
BROKER_URL = u"amqp://"
CELERY_TASK_RESULT_EXPIRES = 10
