import os
from celery import Celery
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csv_generator.settings')
 
app = Celery('csv_generator')
app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])
 
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()