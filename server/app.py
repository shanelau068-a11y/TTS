"""Free Microsoft Edge TTS backend for the GitHub Pages front end."""
from __future__ import annotations

import os
import re

# Keep local development traffic out of common desktop proxy applications.
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1,::1")

import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field

app = FastAPI(title="声场 Edge TTS")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class Segment(BaseModel):
    text: str = Field(min_length=1, max_length=3500)
    voice: str = Field(default="zh-CN-YunxiNeural", min_length=3, max_length=100)


class SynthesisRequest(BaseModel):
    segments: list[Segment] = Field(min_length=1, max_length=300)
    rate: int = Field(default=0, ge=-50, le=50)
    pitch: int = Field(default=0, ge=-20, le=20)


def edge_rate(rate: int) -> str:
    return f"{rate:+d}%"


def edge_pitch(pitch: int) -> str:
    return f"{pitch:+d}Hz"


async def make_mp3(segment: Segment, rate: int, pitch: int) -> bytes:
    audio = bytearray()
    try:
        stream = edge_tts.Communicate(
            segment.text,
            voice=segment.voice,
            rate=edge_rate(rate),
            pitch=edge_pitch(pitch),
        )
        async for event in stream.stream():
            if event["type"] == "audio":
                audio.extend(event["data"])
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"微软语音服务请求失败：{exc}") from exc
    if not audio:
        raise HTTPException(status_code=502, detail="微软语音服务没有返回音频")
    return bytes(audio)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/edge-tts")
async def synthesize(request: SynthesisRequest) -> Response:
    # Front end already breaks at punctuation. Concatenating MP3 frames is supported by players
    # and avoids adding silence or re-encoding artifacts between dialogue lines.
    audio = bytearray()
    for segment in request.segments:
        if not re.search(r"[\w\u4e00-\u9fff]", segment.text):
            continue
        audio.extend(await make_mp3(segment, request.rate, request.pitch))
    if not audio:
        raise HTTPException(status_code=400, detail="没有可朗读的文本")
    return Response(bytes(audio), media_type="audio/mpeg", headers={"Content-Disposition": 'inline; filename="edge-tts.mp3"'})
