import asyncio
import asyncpg
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

async def verify_database_connection():
    try:
        # Convert port to integer
        port = int(os.getenv("POSTGRES_PORT", "5432"))
        
        conn = await asyncpg.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
            host=os.getenv("POSTGRES_HOST"),
            port=port
        )
        
        # Test the connection
        await conn.execute('SELECT 1')
        await conn.close()
        
        logger.info("✅ Database connection test successful!")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection test failed: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(verify_database_connection())