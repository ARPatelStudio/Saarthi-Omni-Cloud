import os
import re
import logging
from groq import Groq
from shared.schemas import BrainMessage
from brains.memory.memory_brain import memory_brain # 🚀 NAYA IMPORT (Memory Engine)

logger = logging.getLogger("AGI_Brain")

# 🚀 Securely load API Key from Render Environment Variables
# NEVER HARDCODE API KEYS IN GITHUB!
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

class AGIBrain:
    def __init__(self):
        if not GROQ_API_KEY:
            logger.error("🚨 GROQ_API_KEY is missing in Render Environment Variables!")
        else:
            self.client = Groq(api_key=GROQ_API_KEY)
            logger.info("🧠 AGI Brain Initialized Successfully.")

    async def process_whatsapp_message(self, message: BrainMessage) -> dict:
        sender_name = message.payload.get("sender", "Unknown")
        incoming_text = message.payload.get("text", "")
        # Phone ki RAM wali temporary history (Short-term)
        short_term_history = message.payload.get("history", "Koi naya notification nahi hai.")

        logger.info(f"AGI Processing WhatsApp message from: {sender_name}")

        # 🚀 THE MAGIC: Fetching Long-Term Memory from Neon DB
        long_term_history = await memory_brain.get_recent_context(sender=sender_name, limit=5)

        system_prompt = f"""
        Tum Jarvis ho, Amit Patel (AR PATEL STUDIO) ke advanced AI Assistant.
        Amit abhi busy hain.
        
        -- LONG-TERM MEMORY (Past Conversations from Database) --
        {long_term_history}
        --------------------------------------------------------
        
        -- SHORT-TERM CONTEXT (Recent Notifications from Phone) --
        {short_term_history}
        ----------------------------------------------------------
        
        Abhi Sender ({sender_name}) ne WhatsApp par naya message bheja hai: "{incoming_text}"

        Task: Ekdam natural, human-like, aur friendly Hinglish (Hindi+English) mein jawab do. Aisa lagna chahiye ki koi asli insaan baat kar raha hai.
        
        Rule 1: Agar History mein tumne already bata diya hai ki Amit busy hain, toh US BAAT KO BILKUL MAT DOHRANA. Seedha past conversation se link karke baat aage badhao.
        Rule 2: AI ya Robot jaisa sound mat karna. "Main AI assistant hoon" bolna band karo agar zaroori na ho.
        Rule 3: Sirf plain text do. Koi JSON, tags (<think>), ya quotes ka use mat karna.
        """

        try:
            # 🚀 Calling Groq API directly from Cloud (Ultra-Fast)
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "[System: Ready for next command]"}
                ],
                model="llama-3.3-70b-versatile", # 🚀 High-speed & Smart model
                temperature=0.7,
                max_tokens=200,
            )
            
            reply_text = chat_completion.choices[0].message.content.strip()
            
            # 🔥 Clean <think> tags safely on Cloud
            reply_text = re.sub(r"<think>[\s\S]*?</think>", "", reply_text).strip()
            reply_text = reply_text.replace('"', '').strip()

            # 🚀 SAVE TO NEON DATABASE (The AGI is learning!)
            await memory_brain.save_interaction(
                device_id=message.source_device, 
                sender=sender_name, 
                user_msg=incoming_text, 
                ai_res=reply_text
            )

            return {
                "source": "AGI_BRAIN",
                "trace_id": message.trace_id,
                "action": "SEND_WHATSAPP_REPLY",
                "response": reply_text
            }

        except Exception as e:
            logger.error(f"❌ Groq API Error: {str(e)}")
            # Intelligent Fallback if API fails
            fallback_text = f"Hello {sender_name}, Amit abhi thode busy hain. Main Jarvis hoon, aapka message un tak pahunch jayega."
            return {
                "source": "AGI_BRAIN",
                "trace_id": message.trace_id,
                "action": "SEND_WHATSAPP_REPLY",
                "response": fallback_text
            }

agi_brain = AGIBrain()
