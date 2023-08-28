from celery.utils.log import get_task_logger
from gspread.exceptions import APIError

from apps.worker.main import celery
import celery as celery_lib
from libs.constants import OperationStatuses
from libs.models import database, Operation, User
from libs.sheets import SheetsClient

logger = get_task_logger(__name__)


@celery.task
def upload_user_operations(user_id: int):
    user = User.get_by_id(user_id)

    operations = list(
        Operation.select().where(Operation.status == OperationStatuses.Finalized, Operation.user_id == user.id)
    )
    if not operations:
        return

    Operation.update(status=OperationStatuses.Processing).where(Operation.id.in_(
        [o.id for o in operations]
    )).execute()

    try:
        SheetsClient(celery.conf["sheet_credentials"], user.sheet).upload_operations(
            operations)
    except APIError as ex:
        Operation.update(status=OperationStatuses.Error).where(Operation.id.in_(
            [o.id for o in operations]
        )).execute()

        logger.exception(ex)
        return

    Operation.update(status=OperationStatuses.Uploaded).where(Operation.id.in_(
        [o.id for o in operations]
    )).execute()


@celery.task
def init_operation_uploading():
    users = list(User.select(User.id).where(User.is_blocked == False, User.sheet.is_null(False)))

    jobs = (upload_user_operations.si(u.id) for u in users)

    task = celery_lib.group(*jobs)
    task.apply_async()
