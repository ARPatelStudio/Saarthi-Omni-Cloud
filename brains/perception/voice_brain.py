import os
import re
import logging
from groq import Groq
from shared.schemas import BrainMessage

# ⚡ AR PATEL STUDIO - VOICE PERCEPTION & CONVERSATION BRAIN
logger = logging.getLogger("VoiceBrain")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

class VoiceBrain:
    def __init__(self):
        if not GROQ_API_KEY:
            logger.error("🚨 GROQ_API_KEY missing for Voice Brain!")
        else:
            self.client = Groq(api_key=GROQ_API_KEY)
            logger.info("🗣️ Voice Brain (Perception) Initialized Successfully.")

    async def process_call_audio(self, message: BrainMessage) -> dict:
        caller_number = message.payload.get("caller", "Unknown Caller")
        caller_text = message.payload.get("transcribed_text", "")
        call_status = message.payload.get("status", "ONGOING") # ONGOING or COMPLETED

        logger.info(f"🗣️ Voice Brain processing call from: {caller_number}")

        # Agar call kat chuki hai, toh summary banayega (Future Update)
        if call_status == "COMPLETED":
            return {
                "source": "VOICE_BRAIN",
                "trace_id": message.trace_id,
                "action": "LOG_AND_NOTIFY",
                "response": "Call ended. Processing summary..."
            }

        # The System Prompt for Live Call (Short, Crisp, Conversational)
        system_prompt = f"""
        Tum Jarvis ho, Amit Patel (AR PATEL STUDIO) ke AI assistant.
        Tumne Amit ka phone uthaya hai kyunki Amit abhi busy hain.
        Caller number: {caller_number}.
        
        Caller ne abhi phone par bola hai: "{caller_text}"
        
        Task: Caller ko ekdam natural, short aur spoken Hinglish (Hindi+English) mein jawab do. 
        Aisa lagna chahiye ki phone par koi asli insaan baat kar raha hai.
        
        Rule 1: Sirf 1 ya 2 chote sentence bolna, kyunki yeh ek live phone call hai. Lamba bhashan mat dena.
        Rule 2: Koi emojis, asterisks (*), ya text formatting use MAT karna. Sirf plain words use karo jo Text-to-Speech engine smoothly bol sake.
        Rule 3: Caller se pooncho ki "Aapka kya message hai, main Amit ji ko bata dunga."
        """

        try:
            # 🚀 Lightning Fast Groq API for Real-Time Call Response
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": "Jaldi aur natural reply do."}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.6,
                max_tokens=100, # Kept short for ultra-low latency
            )
            
            reply_text = chat_completion.choices[0].message.content.strip()
            
            # Remove any think tags or quotes
            reply_text = re.sub(r"<think>[\s\S]*?</think>", "", reply_text).strip()
            reply_text = reply_text.replace('"', '').strip()

            return {
                "source": "VOICE_BRAIN",
                "trace_id": message.trace_id,
                "action": "SPEAK_CALL_RESPONSE",
                "response": reply_text
            }

        except Exception as e:
            logger.error(f"❌ Voice Brain Error: {str(e)}")
            return {
                "source": "VOICE_BRAIN",
                "trace_id": message.trace_id,
                "action": "SPEAK_CALL_RESPONSE",
                "response": "Maaf kijiye, thoda network issue hai. Aap apna message WhatsApp par bhej dijiye."
            }

voice_brain = VoiceBrain()
