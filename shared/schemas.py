from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class DeviceAuth(BaseModel):
    device_id: str = Field(..., description="Unique ID of the device (e.g., PHONE_AMIT_001)")
    auth_token: str = Field(..., description="Secure JWT or API Key for validation")
    device_type: str = Field(..., description="E.g., ANDROID_PHONE, PC, TV")

class BrainMessage(BaseModel):
    trace_id: str = Field(..., description="Unique ID for tracking the request")
    source_device: str = Field(..., description="Which device sent this")
    target_brain: str = Field(default="MASTER_ROUTER", description="Which brain should process this")
    event_type: str = Field(..., description="E.g., TEXT_COMMAND, VISION_FRAME, SENSOR_DATA")
    payload: Dict[str, Any] = Field(default_factory=dict, description="The actual data/message")
    urgency: str = Field(default="NORMAL", description="LOW, NORMAL, HIGH, CRITICAL")
