"""
Main entry point for Telegram bot.
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers import start, schools, instructors, certificate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main bot function."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment variables!")
        return
    
    # Initialize bot and dispatcher
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register routers
    dp.include_router(start.router)
    dp.include_router(schools.router)
    dp.include_router(instructors.router)
    dp.include_router(certificate.router)
    
    logger.info("Bot started!")
    
    # Start polling
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")

