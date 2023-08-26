import logging

from celery import Celery
from celery.signals import worker_process_init, setup_logging, after_setup_task_logger
from playhouse.pool import PooledPostgresqlExtDatabase

from libs.models import database
from apps.scheduler import celeryconfig

celery = Celery()
celery.config_from_object(celeryconfig)


def _init_database(app):
    database.initialize(PooledPostgresqlExtDatabase(**app.conf["postgres_config"]))


@worker_process_init.connect
def initialize(*args, **kwargs):
    _init_database(celery)
