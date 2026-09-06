import logging
from shared.schemas import BrainMessage
from brains.cognition.agi_brain import agi_brain  # 🚀 Import the new Brain!

# ⚡ AR PATEL STUDIO - MASTER UNDERSTANDING ROUTER
logger = logging.getLogger("MasterRouter")

class MasterDispatcher:
    def __init__(self):
        logger.info("🟢 Master Dispatcher Initialized.")

    async def route_event(self, message: BrainMessage) -> dict:
        """
        Receives validated Pydantic model and routes to the appropriate Brain.
        """
        logger.info(f"🧠 Routing Event [{message.event_type}] from {message.source_device}")

        # Future Scope: Yahan if/else ya NLP intent classifier lagega jo alag-alag brains ko call karega
        
        # 🚀 Route WhatsApp Messages directly to AGI Brain
        if message.event_type == "WHATSAPP_MESSAGE":
            return await agi_brain.process_whatsapp_message(message)
            
        # 🫀 Keeps the connection alive
        elif message.event_type == "HEARTBEAT":
            return {
                "source": "MASTER_ROUTER",
                "trace_id": message.trace_id,
                "action": "ACK",
                "response": "Heartbeat received. Engine Online."
            }
            
        # 🛡️ PURANA CODE ZINDA HAI (Backward Compatibility ke liye)
        elif message.event_type == "TEXT_COMMAND":
            return await self._route_to_agi_brain(message)
            
        elif message.event_type == "VISION_FRAME":
            return await self._route_to_vision_brain(message)
            
        else:
            return {"status": "error", "message": "Unknown event type."}

    # ==========================================
    # 🛡️ LEGACY/OLD BRAIN ROUTING (PRESERVED)
    # ==========================================
    async def _route_to_agi_brain(self, message: BrainMessage) -> dict:
        # Phase 2 mein yahan Groq/LLM integration aayega
        logger.info("Forwarding to AGI Brain...")
        user_text = message.payload.get("text", "")
        
        # Simulated Response for Phase 1
        return {
            "source": "AGI_BRAIN",
            "trace_id": message.trace_id,
            "response": f"Boss, I received your command: '{user_text}'. AGI is ready.",
            "action": "SPEAK"
        }

    async def _route_to_vision_brain(self, message: BrainMessage) -> dict:
        logger.info("Forwarding to Vision Brain...")
        return {
            "source": "VISION_BRAIN",
            "trace_id": message.trace_id,
            "response": "Vision processed.",
            "action": "LOG"
        }

master_dispatcher = MasterDispatcher()
