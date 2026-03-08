# DeLuxTTS OpenAI-Compatible API - Quick Start

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd /home/op/DeLuxTTS
pip install -r requirements.txt
pip install -r requirements-server.txt
```

### 2. Start the Server
```bash
# Option 1: Using the start script
./start_server.sh

# Option 2: Direct Python
python server.py

# Option 3: With uvicorn (for development)
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Test the API
```bash
# List available voices
curl http://localhost:8000/v1/voices

# Generate speech with default voice (alloy)
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "delux-tts",
    "input": "Hello from DeLuxTTS!",
    "voice": "alloy"
  }' \
  --output speech.wav
```

## 🎤 Available Voices

10 pre-loaded voices ready to use:

| Voice | Description | Best For |
|-------|-------------|----------|
| `alloy` | British male | Professional content |
| `echo` | British female | Narration |
| `emma` | American female | Conversational |
| `grace` | American female (clear) | Presentations |
| `davis` | American male | Podcasts |
| `fable` | Neutral | General purpose |
| `shimmer` | Neutral alternative | General purpose |
| `onyx` | Spanish male | Spanish content |
| `nova` | Argentinian female | Spanish (AR) content |
| `sakura` | Japanese female | Japanese content |

## 📖 Examples

### Python with OpenAI SDK
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)

# Generate speech
response = client.audio.speech.create(
    model="delux-tts",
    voice="emma",
    input="Hello! This is a test."
)

response.stream_to_file("output.wav")
```

### Test Multiple Voices
```bash
# Run the test script
python test_api.py
```

### Upload Custom Voice
```bash
# Upload your voice
curl -X POST "http://localhost:8000/v1/voices/upload" \
  -F "file=@my_voice.wav" \
  -F "voice_id=my_voice"

# Use it
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "delux-tts",
    "input": "Custom voice test",
    "voice": "my_voice"
  }' \
  --output custom.wav
```

## 🔧 API Endpoints

- `GET /` - Health check
- `GET /v1/models` - List models
- `GET /v1/voices` - List available voices
- `POST /v1/audio/speech` - Generate speech (OpenAI-compatible)
- `POST /v1/audio/speech/file` - Generate with inline file upload
- `POST /v1/voices/upload` - Upload custom voice

## 📝 Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | string | "delux-tts" | Model to use |
| `input` | string | required | Text to convert |
| `voice` | string | "alloy" | Voice ID |
| `response_format` | string | "wav" | Output format (wav/mp3) |
| `speed` | float | 1.0 | Speed multiplier |
| `num_steps` | int | 4 | Quality steps (3-4 best) |
| `guidance_scale` | float | 3.0 | Guidance scale |
| `t_shift` | float | 0.5 | Temperature shift |

## 🛠️ Troubleshooting

### Server won't start
```bash
# Check if port is in use
lsof -i :8000

# Kill existing process
kill -9 $(lsof -t -i:8000)
```

### CUDA errors
The server will automatically fall back to CPU if CUDA is unavailable.

### Voice not found
```bash
# Check available voices
curl http://localhost:8000/v1/voices
```

## 📚 Full Documentation

See `API_README.md` for complete API documentation.
