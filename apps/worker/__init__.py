from celery import Celery
from playhouse.pool import PooledPostgresqlExtDatabase

from libs.models import database


def _init_database(celery):
    database.initialize(PooledPostgresqlExtDatabase(**celery.conf["postgres_config"]))


def create_app(config):
    celery = Celery()
    celery.config_from_object(config)

    _init_database(celery)

    return celery
