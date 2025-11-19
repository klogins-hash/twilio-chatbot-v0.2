#!/usr/bin/env python3
"""Simple Twilio Media Streams bot without Pipecat"""

import asyncio
import base64
import json
import os
from fastapi import FastAPI, WebSocket
from fastapi.responses import Response
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Track active calls
active_calls = {}

@app.get("/")
async def root():
    return {"status": "Simple Twilio bot running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle Twilio Media Stream WebSocket connection"""
    await websocket.accept()
    print("WebSocket connection accepted")

    stream_sid = None
    call_sid = None

    try:
        async for message in websocket.iter_text():
            data = json.loads(message)
            event_type = data.get('event')

            print(f"Received event: {event_type}")

            if event_type == 'start':
                # Extract call information
                stream_sid = data['start']['streamSid']
                call_sid = data['start']['callSid']
                print(f"Call started - SID: {call_sid}, Stream: {stream_sid}")

                # Send a simple audio response (mark message to indicate we're ready)
                response = {
                    "event": "mark",
                    "streamSid": stream_sid,
                    "mark": {
                        "name": "greeting_sent"
                    }
                }
                await websocket.send_text(json.dumps(response))
                print("Sent mark event")

            elif event_type == 'media':
                # Received audio from caller
                payload = data['media']['payload']
                # This is base64 encoded mulaw audio at 8kHz
                print(f"Received audio chunk: {len(payload)} bytes")

            elif event_type == 'stop':
                print(f"Call ended: {call_sid}")
                break

    except Exception as e:
        print(f"Error in WebSocket: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("WebSocket connection closed")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
