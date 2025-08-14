# services/scheduler_service.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from sqlalchemy.ext.asyncio import AsyncSession
from slack_sdk.web.async_client import AsyncWebClient

from core.config import settings
from db.models import Implementation
from db.session import AsyncSessionLocal
from sqlalchemy import select

# --- The actual task the scheduler will run ---

async def send_daily_processing_prompt(client: AsyncWebClient, logger):
    """
    Finds all active users in Stage 1 and sends them the daily prompt.
    """
    logger.info("Scheduler running: `send_daily_processing_prompt`")
    async with AsyncSessionLocal() as session:
        # Find all implementations currently in Stage 1
        stmt = select(Implementation).where(Implementation.stage == "S1")
        result = await session.execute(stmt)
        active_implementations = result.scalars().all()

        for impl in active_implementations:
            try:
                await client.chat_postMessage(
                    channel=impl.owner_user_id,
                    text="Good morning! ☀️ Daily Processing starts in 5 minutes. Target opens today: 3. Ready to start?"
                    # In the next step, we will add interactive buttons here.
                )
                logger.info(f"Sent daily prompt to user {impl.owner_user_id}")
            except Exception as e:
                logger.error(f"Failed to send daily prompt to {impl.owner_user_id}: {e}")

# --- Scheduler Configuration ---

def initialize_scheduler(client: AsyncWebClient, logger):
    """Initializes and starts the APScheduler."""
    
    # Configure the job store to use our existing database for persistence
    jobstores = {
        'default': SQLAlchemyJobStore(url=settings.DATABASE_URL.replace("+asyncpg", ""))
    }
    
    scheduler = AsyncIOScheduler(jobstores=jobstores, timezone="Asia/Dubai")
    
    # Add the daily job
    scheduler.add_job(
        send_daily_processing_prompt,
        trigger='cron',
        hour=9,
        minute=0,
        id='daily_processing_prompt_job',
        replace_existing=True,
        args=[client, logger]
    )
    
    scheduler.start()
    logger.info("Scheduler started successfully. Daily job scheduled for 09:00 GST.")
    return scheduler