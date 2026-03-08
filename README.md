# LuxTTS
<p align="center">
  <a href="https://huggingface.co/YatharthS/LuxTTS">
    <img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Model-FFD21E" alt="Hugging Face Model">
  </a>
  &nbsp;
  <a href="https://huggingface.co/spaces/YatharthS/LuxTTS">
    <img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Space-blue" alt="Hugging Face Space">
  </a>
  &nbsp;
  <a href="https://colab.research.google.com/drive/1cDaxtbSDLRmu6tRV_781Of_GSjHSo1Cu?usp=sharing">
    <img src="https://img.shields.io/badge/Colab-Notebook-F9AB00?logo=googlecolab&logoColor=white" alt="Colab Notebook">
  </a>
</p>

LuxTTS is an lightweight zipvoice based text-to-speech model designed for high quality voice cloning and realistic generation at speeds exceeding 150x realtime.

https://github.com/user-attachments/assets/a3b57152-8d97-43ce-bd99-26dc9a145c29


### The main features are
- 🎯 **OpenAI-Compatible API**: Full REST API server with OpenAI SDK compatibility
- 🎤 **10 Pre-loaded Voices**: Ready-to-use voices in multiple languages (no upload needed)
- 🔊 Voice cloning: SOTA voice cloning on par with models 10x larger
- 🎵 Clarity: Clear 48khz speech generation unlike most TTS models which are limited to 24khz
- ⚡ Speed: Reaches speeds of 150x realtime on a single GPU and faster then realtime on CPU's as well
- 💾 Efficiency: Fits within 1gb vram meaning it can fit in any local gpu

## 🚀 NEW: OpenAI-Compatible API Server

**FastAPI server with full OpenAI SDK compatibility!**

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-server.txt

# Start server (port 8880)
python server.py

# Or use the startup script
./start_server.sh
```

### Available Voices (10 Pre-loaded)
| Voice | Language | Description |
|-------|----------|-------------|
| alloy | English (UK) | British male voice |
| echo | English (UK) | British female voice |
| emma | English (US) | American female voice |
| grace | English (US) | American female voice (clear) |
| davis | English (US) | American male voice |
| fable | English | Neutral voice |
| shimmer | English | Alternative neutral |
| onyx | Spanish | Spanish male voice |
| nova | Spanish (AR) | Argentinian female voice |
| sakura | Japanese | Japanese female voice |

### Usage Examples

**curl:**
```bash
# List voices
curl http://localhost:8880/v1/voices

# Generate speech
curl -X POST "http://localhost:8880/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{"model": "delux-tts", "input": "Hello!", "voice": "alloy"}' \
  --output speech.wav
```

**Python with OpenAI SDK:**
```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8880/v1", api_key="not-needed")

response = client.audio.speech.create(
    model="delux-tts",
    voice="emma",
    input="Hello from DeLuxTTS!"
)
response.stream_to_file("output.wav")
```

**Upload Custom Voice:**
```bash
curl -X POST "http://localhost:8880/v1/voices/upload" \
  -F "file=@my_voice.wav" \
  -F "voice_id=my_voice"
```

📖 **Full API Documentation:** See [API_README.md](API_README.md) | [QUICKSTART.md](QUICKSTART.md) | [VOICES.md](VOICES.md)

---
You can try it locally, colab, or spaces.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1cDaxtbSDLRmu6tRV_781Of_GSjHSo1Cu?usp=sharing)
[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-sm.svg)](https://huggingface.co/spaces/YatharthS/LuxTTS)

#### Simple installation:
```
git clone https://github.com/ysharma3501/LuxTTS.git
cd LuxTTS
pip install -r requirements.txt
```

#### Load model:
```python
from zipvoice.luxvoice import LuxTTS

# load model on GPU
lux_tts = LuxTTS('YatharthS/LuxTTS', device='cuda')

# load model on CPU
# lux_tts = LuxTTS('YatharthS/LuxTTS', device='cpu', threads=2)

# load model on MPS for macs
# lux_tts = LuxTTS('YatharthS/LuxTTS', device='mps')

# load model with OpenVINO (Intel hardware: CPU / Iris Xe GPU / NPU)
# pip install onnxruntime-openvino   # install once, replaces onnxruntime
# lux_tts = LuxTTS('YatharthS/LuxTTS', device='openvino', openvino_device='GPU')
```

#### Simple inference
```python
import soundfile as sf
from IPython.display import Audio

text = "Hey, what's up? I'm feeling really great if you ask me honestly!"

## change this to your reference file path, can be wav/mp3
prompt_audio = 'audio_file.wav'

## encode audio(takes 10s to init because of librosa first time)
encoded_prompt = lux_tts.encode_prompt(prompt_audio, rms=0.01)

## generate speech
final_wav = lux_tts.generate_speech(text, encoded_prompt, num_steps=4)

## save audio
final_wav = final_wav.numpy().squeeze()
sf.write('output.wav', final_wav, 48000)

## display speech
if display is not None:
  display(Audio(final_wav, rate=48000))
```

#### Inference with sampling params:
```python
import soundfile as sf
from IPython.display import Audio

text = "Hey, what's up? I'm feeling really great if you ask me honestly!"

## change this to your reference file path, can be wav/mp3
prompt_audio = 'audio_file.wav'

rms = 0.01 ## higher makes it sound louder(0.01 or so recommended)
t_shift = 0.9 ## sampling param, higher can sound better but worse WER
num_steps = 4 ## sampling param, higher sounds better but takes longer(3-4 is best for efficiency)
speed = 1.0 ## sampling param, controls speed of audio(lower=slower)
return_smooth = False ## sampling param, makes it sound smoother possibly but less cleaner
ref_duration = 5 ## Setting it lower can speedup inference, set to 1000 if you find artifacts.

## encode audio(takes 10s to init because of librosa first time)
encoded_prompt = lux_tts.encode_prompt(prompt_audio, duration=ref_duration, rms=rms)

## generate speech
final_wav = lux_tts.generate_speech(text, encoded_prompt, num_steps=num_steps, t_shift=t_shift, speed=speed, return_smooth=return_smooth)

## save audio
final_wav = final_wav.numpy().squeeze()
sf.write('output.wav', final_wav, 48000)

## display speech
if display is not None:
  display(Audio(final_wav, rate=48000))
```

## Tips
- Please use at minimum a 3 second audio file for voice cloning.
- You can use return_smooth = True if you hear metallic sounds.
- Lower t_shift for less possible pronunciation errors but worse quality and vice versa.

## Inconsistencies and improvement notes

- **Inconsistency:** Inference defaults to float32, while Ampere GPUs can accelerate float32 matmul/conv via TF32 with negligible quality impact for TTS inference.
  - **Improvement added:** TF32 is now enabled automatically on Ampere (`sm_80+`) in GPU model loading.
  ```python
  if major >= 8:
      torch.backends.cuda.matmul.allow_tf32 = True
      torch.backends.cudnn.allow_tf32 = True
      torch.set_float32_matmul_precision("high")
  ```
- **Inconsistency:** Speed guidance is generic and does not call out Ampere-safe optimization path separately from more aggressive fp16 paths.
  - **Suggested usage snippet (quality-preserving on Ampere):**
  ```python
  from zipvoice.luxvoice import LuxTTS

  lux_tts = LuxTTS("YatharthS/LuxTTS", device="cuda")
  # On Ampere, TF32 is enabled automatically in model loading.
  ```

  
## Info

Q: How is this different from ZipVoice?

A: LuxTTS uses the same architecture but distilled to 4 steps with an improved sampling technique. It also uses a custom 48khz vocoder instead of the default 24khz version.

Q: Can it be even faster?

A: Yes, currently it uses float32. Float16 should be significantly faster(almost 2x).

## Roadmap

- [x] Release model and code
- [x] Huggingface spaces demo
- [x] Release MPS support (thanks to @builtbybasit)
- [x] OpenVINO support for Intel CPU / Iris Xe GPU / NPU (i5-1240P and similar)
- [x] **NEW: OpenAI-compatible API server with 10 pre-loaded voices**
- [x] **NEW: REST API endpoints (/v1/audio/speech, /v1/voices, /v1/models)**
- [ ] Release LuxTTS v1.5
- [ ] Release code for float16 inference

## Acknowledgments

### Original Creators
- **Yatharth Sharma** ([@ysharma3501](https://github.com/ysharma3501)) - Original LuxTTS creator
  - Email: yatharthsharma350@gmail.com
  - HuggingFace: [YatharthS/LuxTTS](https://huggingface.co/YatharthS/LuxTTS)

### Core Technologies
- [ZipVoice](https://github.com/k2-fsa/ZipVoice) for their excellent code and model architecture
- [Vocos](https://github.com/gemelo-ai/vocos.git) for the high-quality 48kHz vocoder

### API Server Extension
The OpenAI-compatible API server was added to make LuxTTS accessible via standard REST APIs and compatible with the OpenAI SDK ecosystem. This enables:
- Easy integration with existing applications
- Standard REST API endpoints
- Multi-language support with pre-loaded voices
- Custom voice upload and management

## License

The model and code are licensed under the Apache-2.0 license. See LICENSE for details.

## Support

- **Original Project:** Stars/Likes on the [original repo](https://github.com/ysharma3501/LuxTTS) would be appreciated!
- **Issues:** For API server issues, please check [API_README.md](API_README.md) first
- **Original Author:** yatharthsharma350@gmail.com
