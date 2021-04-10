import os

import redis
from rq import Worker, Queue, Connection
import json
from urllib.parse import urlparse

listen = ['default']
redis_url = os.getenv('REDIS_TLS_URL')

url = urlparse(redis_url)
conn = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)
q = Queue(connection=conn)

if __name__ == '__main__':
    print(f"Existing queue count: {q.count}")
    # print(f"Clearing queue")
    # q.empty()
    print(f"New queue count: {q.count}")
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
