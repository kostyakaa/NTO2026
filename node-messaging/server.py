import asyncio
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any

app = FastAPI()

NODES = ["car", "drone", "manipulator"]

buffers: Dict[str, List[dict]] = {
    node: [] for node in NODES
}

events: Dict[str, asyncio.Event] = {
    node: asyncio.Event() for node in NODES
}


class SendMessage(BaseModel):
    sender_id: str
    recipient_id: str  # конкретный id или "all"
    payload: Dict[str, Any]


@app.post("/send")
def send_message(data: SendMessage):

    if data.sender_id not in NODES:
        raise HTTPException(status_code=400, detail="Unknown sender")

    # broadcast
    if data.recipient_id == "all":
        for node in NODES:
            _push(node, data.sender_id, data.payload)
        return {"status": "sent_to_all"}

    # обычная отправка
    if data.recipient_id not in NODES:
        raise HTTPException(status_code=400, detail="Unknown recipient")

    _push(data.recipient_id, data.sender_id, data.payload)

    return {"status": "sent"}


@app.get("/read")
async def read_messages(
    node_id: str,
    long_polling: bool = Query(False),
    timeout: int = Query(30)
):

    if node_id not in NODES:
        raise HTTPException(status_code=400, detail="Unknown node")

    if long_polling and not buffers[node_id]:
        try:
            await asyncio.wait_for(events[node_id].wait(), timeout=timeout)
        except asyncio.TimeoutError:
            return {"messages": []}

    messages = buffers[node_id]
    buffers[node_id] = []

    events[node_id].clear()

    return {"messages": messages}


def _push(node_id: str, sender: str, payload: dict):
    buffers[node_id].append({
        "from": sender,
        "payload": payload
    })
    events[node_id].set()
