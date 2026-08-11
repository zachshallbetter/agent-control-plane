#!/usr/bin/env python3
import sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from delivery import DeliverySpool
from retry import RetryPolicy

with tempfile.TemporaryDirectory() as directory:
    spool=DeliverySpool(str(Path(directory)/'deliveries.sqlite3'))
    assert spool.enqueue('d1','issues',{'number':1}) is True
    assert spool.enqueue('d1','issues',{'number':1}) is False
    item=spool.claim()[0]; assert item['attempt']==1
    assert spool.finish('d1',False,'transient')=='queued'
    assert RetryPolicy(max_attempts=2).can_retry(1,True) is True
print('runtime tests passed')
