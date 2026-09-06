import logging
import json
from fastapi import WebSocket, WebSocketDisconnect
from shared.schemas import BrainMessage
from core_router.master_dispatcher import master_dispatcher

logger = logging.getLogger("WSS_Gateway")

class ConnectionManager:
    def __init__(self):
        # Stores active connections: {"PHONE_AMIT_001": websocket}
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, device_id: str):
        await websocket.accept()
        self.active_connections[device_id] = websocket
        logger.info(f"🔗 Device Connected: {device_id} | Total Active: {len(self.active_connections)}")

    def disconnect(self, device_id: str):
        if device_id in self.active_connections:
            del self.active_connections[device_id]
            logger.warning(f"🔴 Device Disconnected: {device_id} | Total Active: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, device_id: str):
        if device_id in self.active_connections:
            await self.active_connections[device_id].send_json(message)
        else:
            logger.error(f"Device {device_id} is offline. Message dropped or queued.")

    async def handle_incoming(self, device_id: str, text_data: str):
        try:
            # Parse and Validate JSON using Pydantic
            raw_dict = json.loads(text_data)
            brain_msg = BrainMessage(**raw_dict)
            
            # Send to Master Router
            router_response = await master_dispatcher.route_event(brain_msg)
            
            # Send result back to the specific device
            await self.send_personal_message(router_response, device_id)
            
        except Exception as e:
            logger.error(f"Invalid message format from {device_id}: {str(e)}")
            await self.send_personal_message({"status": "error", "reason": "Invalid JSON or Schema mismatch"}, device_id)

gateway_manager = ConnectionManager()
