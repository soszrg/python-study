### window下使用prefork启动celery，生产程序得不到执行结果
#### 问题描述：
- window下使用prefork启动celery，代码如下：

```
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery("zrg2017031201",
             broker="amqp://guest:guest@localhost:5672//",
             backend="redis://localhost:6379/0")

@app.task()
def hello():
    return 1+2

```

- 使用如下命令启动
```
celery worker -A celery_study.code -l info
```
- 此时如果调用hello.delay()，任务可以执行，但不能取到result值，status一直为pending，如下：
```
[2017-03-12 18:04:34,891: INFO/MainProcess] Received task: celery_study.code.celery.hello[47c57316-995e-43c5-96a7-0fa4c9243f96]
[2017-03-12 18:04:34,905: INFO/MainProcess] Task celery_study.code.celery.hello[47c57316-995e-43c5-96a7-0fa4c9243f96] succeeded in 0.0119998455048s: 3

```
```
In[10]: re=hello.delay()
In[11]: re.status
Out[11]: 
'PENDING'
In[12]: re.result
```

- 原因：应该是windows下的prefork导致的，celery启动时，默认为prefork模式，具体原因不详
- 解决方法1：启动时指定非prefork的pool（如下），也可以是gevent或者threads
```
celery worker -A celery_study.code -l info --pool=eventlet

```
- 解决方法2：将配置信息放在单独的配置文件里，通过config_from_object方法载入