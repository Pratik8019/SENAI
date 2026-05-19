"""
SentinelAI — WebSocket Handler

Real-time updates for the dashboard.
"""

import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set

router = APIRouter()

# Connected clients
connected_clients: Set[WebSocket] = set()


@router.websocket("/ws/updates")
async def websocket_updates(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)

    try:
        while True:
            # Keep connection alive, listen for client messages
            data = await websocket.receive_text()
            # Echo back acknowledgment
            await websocket.send_json({"type": "ack", "data": data})
    except WebSocketDisconnect:
        connected_clients.discard(websocket)


async def broadcast_update(event_type: str, data: dict):
    """Broadcast an update to all connected WebSocket clients."""
    message = json.dumps({"type": event_type, "data": data})
    disconnected = set()

    for ws in connected_clients:
        try:
            await ws.send_text(message)
        except Exception:
            disconnected.add(ws)

    connected_clients.difference_update(disconnected)
