# Available Voices

## Default Voices (Pre-loaded)

The server comes with **10 pre-loaded voices** that are automatically available when the server starts.

### Voice List

| Voice ID | File | Description | Language | Source |
|----------|------|-------------|----------|--------|
| `alloy` | alloy.wav | British male voice | English (UK) | britishMan.wav |
| `echo` | echo.wav | British female voice | English (UK) | britishWoman.wav |
| `fable` | fable.wav | Default neutral voice | English | default_voice.wav |
| `onyx` | onyx.wav | Spanish male voice | Spanish | CordobesMan.wav |
| `nova` | nova.wav | Argentinian female voice | Spanish (AR) | es-Argentinian_female.wav |
| `shimmer` | fable.wav | Alternative neutral voice | English | (alias of fable) |
| `emma` | emma.wav | American female voice | English (US) | en-Emma_woman.wav |
| `grace` | grace.wav | American female voice (clear) | English (US) | en-Grace_woman.wav |
| `davis` | davis.wav | American male voice | English (US) | en-Davis_man.wav |
| `sakura` | sakura.wav | Japanese female voice | Japanese | jp-Spk1_woman.wav |

### Usage Examples

```bash
# British male
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{"model": "delux-tts", "input": "Hello!", "voice": "alloy"}' \
  --output alloy.wav

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

## Custom Voices

You can upload your own voice files for cloning:

```bash
# Upload a custom voice
curl -X POST "http://localhost:8000/v1/voices/upload" \
  -F "file=@my_voice.wav" \
  -F "voice_id=my_custom_voice"

# Use the custom voice
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{"model": "delux-tts", "input": "Test", "voice": "my_custom_voice"}' \
  --output custom.wav
```

## Tips for Best Results

1. **Audio Quality**: Use high-quality audio files (minimum 3 seconds)
2. **Voice Matching**: Choose voices that match your content's language/accent
3. **Clarity**: For voice cloning, use clear recordings without background noise
4. **Duration**: Reference audio should be 3-10 seconds for best results

## Adding More Voices

To add more default voices:

1. Copy your `.wav` file to `/home/op/DeLuxTTS/default_voices/`
2. Update the `DEFAULT_VOICES` dictionary in `server.py`
3. Restart the server

Example:
```python
DEFAULT_VOICES["new_voice"] = {
    "file": "new_voice.wav",
    "description": "Description of the voice"
}
```
