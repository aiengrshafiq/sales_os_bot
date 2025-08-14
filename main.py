# main.py
import asyncio
from fastapi import FastAPI, Request
from sqlalchemy import select
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_sdk.web.async_client import AsyncWebClient

from core.config import settings
from services.slack_service import create_scp_onboarding_modal
from db.models import Implementation, SCPProfile
from db.session import AsyncSessionLocal # <-- THE CRITICAL MISSING IMPORT

from services.scheduler_service import initialize_scheduler

# Initialize the Slack Bolt App
slack_app = AsyncApp(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_SIGNING_SECRET
)

# Create a handler to bridge FastAPI and Slack Bolt
app_handler = AsyncSlackRequestHandler(slack_app)

# Initialize the FastAPI app
api = FastAPI(title="Sales-OS Bot")


# --- MODIFIED: Add a startup event handler ---

@api.on_event("startup")
async def startup_event():
    """Initializes the scheduler when the application starts."""
    initialize_scheduler(client=slack_app.client, logger=slack_app.logger)

    
async def process_scp_submission(user_id: str, view: dict, client: AsyncWebClient, logger):
    """
    This background function is now fully asynchronous, including DB calls.
    """
    try:
        values = view["state"]["values"]
        offer = values["offer_block"]["offer_input"]["value"]
        price_band = values["price_band_block"]["price_band_input"]["value"]
        icp = values["icp_block"]["icp_input"]["value"]
        
        scp_data = {"primary_offer": offer, "price_band": price_band, "icp": icp}
        logger.info(f"Async Task: Processing SCP submission for {user_id}")

        # Use the new async session maker (this will now work)
        async with AsyncSessionLocal() as session:
            stmt = select(Implementation).where(Implementation.owner_user_id == user_id)
            result = await session.execute(stmt)
            implementation = result.scalar_one_or_none()

            if not implementation:
                implementation = Implementation(owner_user_id=user_id, stage="S1")
                session.add(implementation)
                await session.flush()

                scp_profile = SCPProfile(implementation_id=implementation.id, profile_data=scp_data)
                session.add(scp_profile)
                await session.commit()

                await client.chat_postMessage(
                    channel=user_id,
                    text="✅ Great! Your Sales-OS profile is set up and you are now in *Stage 1: Instrument & Initiate*. Your daily prompts will begin shortly."
                )
            else:
                await client.chat_postMessage(
                    channel=user_id,
                    text="Looks like you're already set up! Use other `/salesos` commands to proceed."
                )

    except Exception as e:
        logger.error(f"Error in asyncio task for {user_id}: {e}")
        await client.chat_postMessage(
            channel=user_id,
            text="❌ There was an error saving your profile in the background. Please try again or contact support."
        )


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


@slack_app.command("/module")
async def handle_module_command(ack, body, client, logger):
    """Handles the /module command to open the onboarding modal."""
    await ack()
    try:
        modal_view = create_scp_onboarding_modal()
        await client.views_open(trigger_id=body["trigger_id"], view=modal_view)
    except Exception as e:
        logger.error(f"Error opening modal: {e}")


@slack_app.view("scp_modal_submission")
async def handle_scp_submission(ack, body, client, logger):
    """
    This handler uses Python's built-in asyncio to run the
    fully asynchronous database operations in the background.
    """
    await ack()
    asyncio.create_task(
        process_scp_submission(
            user_id=body["user"]["id"],
            view=body["view"],
            client=client,
            logger=logger
        )
    )