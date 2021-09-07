from app import celery
from datetime import datetime
import os

@celery.task()
def make_file(fname, content):
    with open(fname, "w") as f:
        f.write(content)
    print("fname: "+fname+" | processed: "+str(datetime.now()))
