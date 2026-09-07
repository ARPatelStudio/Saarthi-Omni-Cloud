import os
import logging
import asyncpg
from datetime import datetime

# ⚡ AR PATEL STUDIO - LONG TERM MEMORY BRAIN (Neon PostgreSQL)
logger = logging.getLogger("MemoryBrain")

# 🚀 Securely load DB URL from Render Environment Variables
NEON_DB_URL = os.environ.get("NEON_DB_URL")

class MemoryBrain:
    def __init__(self):
        self.pool = None
        if not NEON_DB_URL:
            logger.warning("⚠️ NEON_DB_URL is missing! Memory Brain will run in offline/dummy mode.")

    async def connect_to_database(self):
        if not self.pool and NEON_DB_URL:
            try:
                # Create a persistent connection pool
                self.pool = await asyncpg.create_pool(NEON_DB_URL)
                
                # 🚀 Auto-Create Table if it doesn't exist
                async with self.pool.acquire() as conn:
                    await conn.execute('''
                        CREATE TABLE IF NOT EXISTS jarvis_long_term_memory (
                            id SERIAL PRIMARY KEY,
                            device_id TEXT,
                            sender_name TEXT,
                            user_message TEXT,
                            ai_response TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    ''')
                logger.info("🧬 Memory Brain Connected to Neon PostgreSQL Successfully.")
            except Exception as e:
                logger.error(f"❌ Failed to connect to Neon DB: {e}")

    async def save_interaction(self, device_id: str, sender: str, user_msg: str, ai_res: str):
        if self.pool:
            try:
                async with self.pool.acquire() as conn:
                    await conn.execute(
                        "INSERT INTO jarvis_long_term_memory (device_id, sender_name, user_message, ai_response) VALUES ($1, $2, $3, $4)",
                        device_id, sender, user_msg, ai_res
                    )
                logger.info(f"💾 Saved conversation with {sender} to Long-Term Memory.")
            except Exception as e:
                logger.error(f"Error saving to memory: {e}")

    async def get_recent_context(self, sender: str, limit: int = 4) -> str:
        """
        Fetches the last few messages of a specific user to give AGI context.
        """
        if not self.pool:
            return "[No long-term memory connection available.]"
        
        try:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(
                    "SELECT user_message, ai_response FROM jarvis_long_term_memory WHERE sender_name = $1 ORDER BY timestamp DESC LIMIT $2",
                    sender, limit
                )
                
                # 🔥 CRITICAL FIX: Removed the "Poison Pill" sentence. 
                # Now it gracefully falls back to short-term memory if DB is empty.
                if not rows:
                    return "[No past long-term memory found for this sender yet. Rely on short-term context.]"
                
                # Reverse to get chronological order (Oldest first, Newest last)
                history = []
                for row in reversed(rows):
                    history.append(f"[{sender}]: {row['user_message']}\n[Jarvis]: {row['ai_response']}")
                
                return "\n".join(history)
        except Exception as e:
            logger.error(f"Error fetching memory: {e}")
            return "[Error retrieving long-term memory.]"

memory_brain = MemoryBrain()
