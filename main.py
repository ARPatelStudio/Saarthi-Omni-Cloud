import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from api.gateway_wss import gateway_manager
from brains.memory.memory_brain import memory_brain # 🚀 NAYA IMPORT

# ⚡ AR PATEL STUDIO - LOGGING CONFIGURATION
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("JarvisOmniCloud")

app = FastAPI(title="Jarvis Omni-Cloud API", version="1.0.0")

# Security: Allow connections from anywhere (Can be restricted later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Jarvis Omni-Cloud Engine Started.")
    # 🚀 CONNECT TO NEON POSTGRESQL ON BOOT
    await memory_brain.connect_to_database()

# 🟢 Render Health Check Endpoint (Render needs this to know the app is alive)
@app.get("/")
async def health_check():
    return {
        "status": "ONLINE",
        "engine": "Jarvis Omni-Cloud Master Router",
        "developer": "AR PATEL STUDIO From India"
    }

# ⚡ The Real-Time WebSocket Gateway
@app.websocket("/ws/jarvis/{device_id}")
async def websocket_endpoint(websocket: WebSocket, device_id: str):
    await gateway_manager.connect(websocket, device_id)
    try:
        while True:
            # Wait for message from Device (Phone/PC/TV)
            data = await websocket.receive_text()
            # Send to Gateway Manager
            await gateway_manager.handle_incoming(device_id, data)
    except WebSocketDisconnect:
        gateway_manager.disconnect(device_id)
