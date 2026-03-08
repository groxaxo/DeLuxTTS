# DeLuxTTS OpenAI-Compatible API Server

This server provides an OpenAI-compatible API for the DeLuxTTS text-to-speech model.

## Installation

```bash
pip install -r requirements.txt
pip install -r requirements-server.txt
```

## Running the Server

```bash
cd /home/op/DeLuxTTS
python server.py
```

Or with uvicorn directly:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

## Available Default Voices

The server comes with 10 pre-loaded voices ready to use:

| Voice ID | Description | Language |
|----------|-------------|----------|
| **alloy** | British male voice | English (UK) |
| **echo** | British female voice | English (UK) |
| **fable** | Default neutral voice | English |
| **onyx** | Spanish male voice | Spanish |
| **nova** | Argentinian female voice | Spanish (AR) |
| **shimmer** | Alternative neutral voice | English |
| **emma** | American female voice | English (US) |
| **grace** | American female voice (clear) | English (US) |
| **davis** | American male voice | English (US) |
| **sakura** | Japanese female voice | Japanese |

## API Endpoints

### OpenAI-Compatible Endpoints

#### GET /v1/voices

List all available voices (default + custom uploaded).

**Example:**
```bash
curl http://localhost:8000/v1/voices
```

#### POST /v1/audio/speech

Generate speech from text using a pre-loaded or uploaded voice.

**Request Body:**
```json
{
  "model": "delux-tts",
  "input": "Hello, this is a test of the DeLuxTTS API.",
  "voice": "alloy",
  "response_format": "wav",
  "speed": 1.0,
  "num_steps": 4,
  "guidance_scale": 3.0,
  "t_shift": 0.5
}
```

**Example with curl (using default voice):**
```bash
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "delux-tts",
    "input": "Hello from DeLuxTTS!",
    "voice": "alloy",
    "response_format": "wav"
  }' \
  --output speech.wav
```

**Example with curl (using different voices):**
```bash
# British female
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{"model": "delux-tts", "input": "Hello love!", "voice": "echo"}' \
  --output echo.wav

# American female
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{"model": "delux-tts", "input": "Hey there!", "voice": "emma"}' \
  --output emma.wav

# Japanese
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{"model": "delux-tts", "input": "こんにちは", "voice": "sakura"}' \
  --output sakura.wav
```

#### POST /v1/audio/speech/file

Generate speech from text with inline voice file upload (for custom voices).

**Example with curl:**
```bash
curl -X POST "http://localhost:8000/v1/audio/speech/file" \
  -F "file=@reference_audio.wav" \
  -F "input=Hello from DeLuxTTS!" \
  -F "response_format=wav" \
  --output speech.wav
```

#### POST /v1/voices/upload

Upload and encode a custom reference voice for later use.

**Parameters:**
- `file`: Audio file (.wav or .mp3)
- `voice_id`: Optional custom ID for the voice (auto-generated if not provided)

**Response:**
```json
{
  "voice_id": "uuid-here",
  "message": "Voice uploaded and encoded successfully"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/v1/voices/upload" \
  -F "file=@my_voice.wav" \
  -F "voice_id=my_custom_voice"
```

#### GET /v1/models

List available models (OpenAI-compatible).

## Using with OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

# Use any of the 10 pre-loaded voices
response = client.audio.speech.create(
    model="delux-tts",
    voice="alloy",  # or echo, fable, onyx, nova, shimmer, emma, grace, davis, sakura
    input="Hello from DeLuxTTS!",
    response_format="wav"
)

response.stream_to_file("output.wav")
```

**Streaming example:**
```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

# Stream directly to file
with client.audio.speech.with_streaming_response.create(
    model="delux-tts",
    voice="emma",
    input="This is a streaming example!",
    response_format="wav"
) as response:
    response.stream_to_file("streaming_output.wav")
```

## Parameters

- **model**: Model to use (default: "delux-tts")
- **input**: Text to convert to speech
- **voice**: Voice ID (from uploaded voices)
- **response_format**: Output format ("wav" or "mp3")
- **speed**: Speech speed multiplier (default: 1.0)
- **num_steps**: Sampling steps, higher = better quality but slower (default: 4)
- **guidance_scale**: Guidance scale for generation (default: 3.0)
- **t_shift**: Sampling parameter, higher can sound better but worse WER (default: 0.5)
- **rms**: Volume/loudness, higher = louder (default: 0.01)
- **duration**: Reference audio duration in seconds (default: 5.0)
- **return_smooth**: Enable smoother audio (default: False)

## Tips

- Use at minimum a 3-second audio file for voice cloning
- Set `return_smooth=True` if you hear metallic sounds
- Lower `t_shift` for fewer pronunciation errors but potentially worse quality
- Recommended `num_steps`: 3-4 for best efficiency/quality balance
