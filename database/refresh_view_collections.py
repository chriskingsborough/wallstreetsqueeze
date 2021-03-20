from rq import Queue
from rq.job import Job
from rq import Retry

import view_collections as vc
from worker import conn

q = Queue(connection=conn)

def refresh_view_collection():
    """Refresh stock info"""

    view_configs = vc.read_yaml()

    for view in view_configs:
        q.enqueue_call(
            func=vc.refresh_view_changes,
            args=(
                view['name'],
                view['limit']
            ),
            retry=Retry(3),
            result_ttl=5000
        )

if __name__ == '__main__':
    refresh_view_collection()
