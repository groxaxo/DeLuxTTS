import io
import tempfile
import uuid
from pathlib import Path
from typing import Optional

import soundfile as sf
import torch
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel

from zipvoice.luxvoice import LuxTTS

app = FastAPI(title="DeLuxTTS API", description="OpenAI-compatible TTS API for DeLuxTTS")

lux_tts = None
voice_cache = {}
default_voices_dir = Path(__file__).parent / "default_voices"

DEFAULT_VOICES = {
    "alloy": {"file": "alloy.wav", "description": "British male voice"},
    "echo": {"file": "echo.wav", "description": "British female voice"},
    "fable": {"file": "fable.wav", "description": "Default neutral voice"},
    "onyx": {"file": "onyx.wav", "description": "Spanish male voice"},
    "nova": {"file": "nova.wav", "description": "Argentinian female voice"},
    "shimmer": {"file": "fable.wav", "description": "Alternative neutral voice"},
    "emma": {"file": "emma.wav", "description": "American female voice"},
    "grace": {"file": "grace.wav", "description": "American female voice (clear)"},
    "davis": {"file": "davis.wav", "description": "American male voice"},
    "sakura": {"file": "sakura.wav", "description": "Japanese female voice"},
}


class SpeechRequest(BaseModel):
    model: str = "delux-tts"
    input: str
    voice: str = "alloy"
    response_format: str = "wav"
    speed: float = 1.0
    num_steps: int = 4
    guidance_scale: float = 3.0
    t_shift: float = 0.5
    rms: float = 0.01
    duration: int = 5
    return_smooth: bool = False


class VoiceUpload(BaseModel):
    voice_id: str
    message: str


@app.on_event("startup")
async def startup_event():
    global lux_tts
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading DeLuxTTS model on {device}...")
    lux_tts = LuxTTS("YatharthS/LuxTTS", device=device)
    print("Model loaded successfully!")

    print("\nLoading default voices...")
    for voice_name, voice_info in DEFAULT_VOICES.items():
        voice_path = default_voices_dir / voice_info["file"]
        if voice_path.exists():
            try:
                encoded_prompt = lux_tts.encode_prompt(str(voice_path), duration=5, rms=0.01)
                voice_cache[voice_name] = encoded_prompt
                print(f"  ✓ Loaded voice: {voice_name} ({voice_info['description']})")
            except Exception as e:
                print(f"  ✗ Failed to load voice {voice_name}: {e}")
        else:
            print(f"  ✗ Voice file not found: {voice_path}")

    print(f"\nTotal voices available: {len(voice_cache)}")


@app.get("/")
async def root():
    return {"message": "DeLuxTTS API", "status": "running"}


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [{"id": "delux-tts", "object": "model", "created": 1234567890, "owned_by": "delux-tts"}],
    }


@app.post("/v1/voices/upload")
async def upload_voice(file: UploadFile = File(...), voice_id: Optional[str] = None):
    if not file.filename or not file.filename.endswith((".wav", ".mp3")):
        raise HTTPException(status_code=400, detail="Only .wav or .mp3 files are supported")

    voice_id = voice_id or str(uuid.uuid4())

    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        encoded_prompt = lux_tts.encode_prompt(tmp_path, duration=5, rms=0.01)
        voice_cache[voice_id] = encoded_prompt

        return {"voice_id": voice_id, "message": "Voice uploaded and encoded successfully"}
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@app.get("/v1/voices")
async def list_voices():
    default_voice_list = [
        {"voice_id": vid, "description": vinfo["description"], "type": "default"}
        for vid, vinfo in DEFAULT_VOICES.items()
        if vid in voice_cache
    ]

    custom_voice_list = [
        {"voice_id": vid, "status": "available", "type": "custom"}
        for vid in voice_cache.keys()
        if vid not in DEFAULT_VOICES
    ]

    return {
        "object": "list",
        "data": default_voice_list + custom_voice_list,
        "default_voices": list(DEFAULT_VOICES.keys()),
    }


@app.post("/v1/audio/speech")
async def create_speech(request: SpeechRequest):
    if lux_tts is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    if request.voice not in voice_cache:
        available_voices = list(DEFAULT_VOICES.keys())
        raise HTTPException(
            status_code=400,
            detail=f"Voice '{request.voice}' not found. Available default voices: {available_voices}. Or upload a custom voice using /v1/voices/upload",
        )

    encoded_prompt = voice_cache[request.voice]

    try:
        final_wav = lux_tts.generate_speech(
            text=request.input,
            encode_dict=encoded_prompt,
            num_steps=request.num_steps,
            guidance_scale=request.guidance_scale,
            t_shift=request.t_shift,
            speed=request.speed,
            return_smooth=request.return_smooth,
        )

        audio_data = final_wav.numpy().squeeze()

        buffer = io.BytesIO()
        sf.write(buffer, audio_data, 48000, format="WAV")
        buffer.seek(0)

        media_type = "audio/wav" if request.response_format == "wav" else "audio/mpeg"

        return StreamingResponse(
            buffer,
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="speech.{request.response_format}"'},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech generation failed: {str(e)}")


@app.post("/v1/audio/speech/file")
async def create_speech_from_file(
    file: UploadFile = File(...),
    input: str = Form(...),
    response_format: str = Form("wav"),
    speed: float = Form(1.0),
    num_steps: int = Form(4),
    guidance_scale: float = Form(3.0),
    t_shift: float = Form(0.5),
    rms: float = Form(0.01),
    duration: int = Form(5),
    return_smooth: bool = Form(False),
):
    if lux_tts is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    if not file.filename or not file.filename.endswith((".wav", ".mp3")):
        raise HTTPException(status_code=400, detail="Only .wav or .mp3 files are supported")

    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        encoded_prompt = lux_tts.encode_prompt(tmp_path, duration=duration, rms=rms)

        final_wav = lux_tts.generate_speech(
            text=input,
            encode_dict=encoded_prompt,
            num_steps=num_steps,
            guidance_scale=guidance_scale,
            t_shift=t_shift,
            speed=speed,
            return_smooth=return_smooth,
        )

        audio_data = final_wav.numpy().squeeze()

        buffer = io.BytesIO()
        sf.write(buffer, audio_data, 48000, format="WAV")
        buffer.seek(0)

        media_type = "audio/wav" if response_format == "wav" else "audio/mpeg"

        return StreamingResponse(
            buffer,
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="speech.{response_format}"'},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech generation failed: {str(e)}")
    finally:
        Path(tmp_path).unlink(missing_ok=True)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8880)
