#!/usr/bin/env python3
"""Simple TwiML server to respond to Twilio voice webhooks"""

from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()

@app.get("/")
@app.post("/")
async def root():
    return {"status": "TwiML server running"}

@app.get("/voice")
@app.post("/voice")
async def voice_webhook():
    """Return TwiML that connects to our WebSocket"""
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="ws://37.27.96.88:7860/ws" />
    </Connect>
</Response>"""

    return Response(content=twiml, media_type="application/xml")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
