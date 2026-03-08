#!/usr/bin/env python3
"""Verify that default voices are properly loaded"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def verify_voices():
    from zipvoice.luxvoice import LuxTTS
    import torch

    print("=" * 60)
    print("DeLuxTTS Voice Verification")
    print("=" * 60)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"\nDevice: {device}")

    print("\nLoading model...")
    lux_tts = LuxTTS("YatharthS/LuxTTS", device=device)
    print("✓ Model loaded")

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

    print(f"\nVerifying {len(DEFAULT_VOICES)} default voices...")
    print("-" * 60)

    success_count = 0
    failed_voices = []

    for voice_name, voice_info in DEFAULT_VOICES.items():
        voice_path = default_voices_dir / voice_info["file"]

        if not voice_path.exists():
            print(f"✗ {voice_name:12} - File not found: {voice_path}")
            failed_voices.append(voice_name)
            continue

        try:
            encoded_prompt = lux_tts.encode_prompt(str(voice_path), duration=5, rms=0.01)
            print(f"✓ {voice_name:12} - {voice_info['description']}")
            success_count += 1
        except Exception as e:
            print(f"✗ {voice_name:12} - Error: {e}")
            failed_voices.append(voice_name)

    print("-" * 60)
    print(f"\nResults: {success_count}/{len(DEFAULT_VOICES)} voices loaded successfully")

    if failed_voices:
        print(f"\nFailed voices: {', '.join(failed_voices)}")
        return False

    print("\n✓ All voices verified successfully!")
    return True


if __name__ == "__main__":
    try:
        success = verify_voices()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Verification failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
