import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from makers.apps.auth import services
from makers.apps.auth.models import User
from makers.apps.commons.constants import TZ
from makers.apps.db.deps import get_db_session

scheduler = AsyncIOScheduler(jobstores={"default": MemoryJobStore()}, timezone="UTC")


async def free_trial_end_task(db: AsyncSession, *, user: User):
    sub_expired_date = user.registered_at + datetime.timedelta(days=14)
    scheduler.add_job(
        services.end_subscription,
        "date",
        run_date=sub_expired_date,
        timezone=TZ,
        args=[db],
        kwargs={"user_id": user.id},
    )
