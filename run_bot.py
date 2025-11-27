"""Run bot with error handling."""
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import TELEGRAM_BOT_TOKEN
from bot.handlers import start, schools, instructors, certificate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

async def main():
    """Main bot function."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment variables!")
        return
    
    try:
        # Initialize bot and dispatcher
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        dp = Dispatcher(storage=MemoryStorage())
        
        # Register routers
        dp.include_router(start.router)
        dp.include_router(schools.router)
        dp.include_router(instructors.router)
        dp.include_router(certificate.router)
        
        logger.info("Bot started!")
        logger.info(f"Bot token: {TELEGRAM_BOT_TOKEN[:10]}...")
        
        # Start polling
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

