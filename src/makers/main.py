import os
import pathlib

import uvicorn
import alembic.config

from makers.apps.commons.tasks import scheduler
from makers.app import app as fastapi


def apply_migrations():
    os.chdir(pathlib.Path(__file__).parent)
    args = [
        '--raiseerr',
        'upgrade', 'heads',
    ]
    alembic.config.main(argv=args)


def execute():
    """
    1. Run FastApi
    2. Apply migrations
    3. Run scheduler
    """
    apply_migrations()

    scheduler.start()

    uvicorn.run(fastapi, host="0.0.0.0", port=8000)
