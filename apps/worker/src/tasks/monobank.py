from datetime import timedelta

import celery as celery_lib
from celery.utils.log import get_task_logger

from apps.worker.main import celery
from libs.constants import OperationTypes, OperationSources
from libs.models.models import database, MonobankIntegration, User, Operation
from libs.monobank import MonobankClient, MonobankError
from libs.utils import get_now

logger = get_task_logger(__name__)


def _format_obj(obj):
    return dict(
        amount=abs(obj["amount"] / 100),
        type=OperationTypes.Expenses if obj["amount"] < 0 else OperationTypes.Income,
        comment=obj.get("description"),
    )


@celery.task
def download_statement(integration_id: int, sampling_time: int, ignored_comments: list = None):
    if ignored_comments is None:
        ignored_comments = []

    integration = MonobankIntegration.get_by_id(integration_id)
    client = MonobankClient(integration.token)

    try:
        resp = client.statement(
            start=(get_now() - timedelta(seconds=sampling_time)), to=get_now()
        )
    except MonobankError as ex:
        logger.error(ex)
        return

    if not resp:
        return

    rows = []
    for obj in resp:
        rows.append(_format_obj(obj))

    for i, obj in enumerate(rows):

        if obj["comment"] in ignored_comments:
            continue

        rows[i].update(
            dict(user_id=integration.user_id, source=OperationSources.Monobank)
        )

    Operation.insert_many(rows).execute()


@celery.task
def init_statements(sampling_time: int):
    integrations = list(
        MonobankIntegration.select(MonobankIntegration.id, MonobankIntegration.user_id)
        .join(User)
        .where(User.is_blocked == False)
    )

    jobs = (download_statement.si(i.id, sampling_time, 
    [
        "future",
        "ignore",
        "На білу картку"
    ]) for i in integrations)

    task = celery_lib.group(*jobs)
    task.apply_async()
