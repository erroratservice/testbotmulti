import asyncio
import importlib
from pyrogram import idle
from bot import bot, LOGGER
from bot.helper.status import status_loop

async def start_services():
    LOGGER.info("---- Starting Bot Farm ----")
    
    # Load Modules Dynamically
    modules = ["count", "cancel", "status_cmd", "settings"]
    for module in modules:
        importlib.import_module(f"bot.modules.{module}")
        LOGGER.info(f"Loaded Module: {module}")

    await bot.start()
    me = await bot.get_me()
    LOGGER.info(f"Main Controller Started as @{me.username}")

    # Start the Status Loop
    asyncio.create_task(status_loop())

    await idle()
    await bot.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
  
