import requests
import sys

BASE_URL = "http://localhost:8000"


def test_health():
    """Test if server is running"""
    response = requests.get(f"{BASE_URL}/")
    print(f"Health check: {response.status_code}")
    print(response.json())
    return response.status_code == 200


def test_upload_voice(audio_file_path: str, voice_id: str = "test_voice"):
    """Upload a voice file"""
    with open(audio_file_path, "rb") as f:
        files = {"file": f}
        data = {"voice_id": voice_id}
        response = requests.post(f"{BASE_URL}/v1/voices/upload", files=files, data=data)

    print(f"Voice upload: {response.status_code}")
    print(response.json())
    return response.status_code == 200


def test_list_voices():
    """List all uploaded voices"""
    response = requests.get(f"{BASE_URL}/v1/voices")
    print(f"List voices: {response.status_code}")
    print(response.json())
    return response.status_code == 200


def test_generate_speech(
    voice_id: str = "alloy",
    text: str = "Hello! This is a test of the DeLuxTTS API.",
    output_file: str = "test_output.wav",
):
    """Generate speech using default or uploaded voice"""
    payload = {
        "model": "delux-tts",
        "input": text,
        "voice": voice_id,
        "response_format": "wav",
        "speed": 1.0,
        "num_steps": 4,
    }

    response = requests.post(f"{BASE_URL}/v1/audio/speech", json=payload, stream=True)

    print(f"Speech generation: {response.status_code}")

    if response.status_code == 200:
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Audio saved to {output_file}")
        return True
    else:
        print(response.text)
        return False


def test_multiple_voices():
    """Test multiple default voices"""
    test_voices = ["alloy", "echo", "emma", "davis"]

    for voice in test_voices:
        print(f"\nTesting voice: {voice}")
        output_file = f"test_output_{voice}.wav"

        if not test_generate_speech(voice, f"Hello, I am {voice}!", output_file):
            print(f"Failed to generate speech with voice: {voice}")
            return False

    print("\n✓ All voice tests passed!")
    return True


def test_generate_speech_with_file(audio_file_path: str, text: str, output_file: str = "test_output_file.wav"):
    """Generate speech with inline file upload"""
    with open(audio_file_path, "rb") as f:
        files = {"file": f}
        data = {"input": text, "response_format": "wav", "speed": 1.0, "num_steps": 4}
        response = requests.post(f"{BASE_URL}/v1/audio/speech/file", files=files, data=data, stream=True)

    print(f"Speech generation with file: {response.status_code}")

    if response.status_code == 200:
        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Audio saved to {output_file}")
        return True
    else:
        print(response.text)
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Testing DeLuxTTS API")
    print("=" * 60)

    if not test_health():
        print("Server is not running! Start it with: python server.py")
        sys.exit(1)

    print("\n" + "=" * 60)
    test_list_voices()

    print("\n" + "=" * 60)
    print("Testing default voices...")
    if not test_multiple_voices():
        print("Failed to test multiple voices")
        sys.exit(1)

    if len(sys.argv) >= 2:
        audio_file = sys.argv[1]
        voice_id = sys.argv[2] if len(sys.argv) > 2 else "custom_voice"

        print("\n" + "=" * 60)
        print("Testing custom voice upload...")
        if not test_upload_voice(audio_file, voice_id):
            print("Failed to upload voice")
            sys.exit(1)

        print("\n" + "=" * 60)
        if not test_generate_speech(voice_id, "Hello! This is a custom voice test."):
            print("Failed to generate speech with custom voice")
            sys.exit(1)

        print("\n" + "=" * 60)
        if not test_generate_speech_with_file(audio_file, "This is another test with inline file upload."):
            print("Failed to generate speech with file")
            sys.exit(1)

    print("\n" + "=" * 60)
    print("All tests passed!")
    print("\nTip: Run with 'python test_api.py <audio_file>' to test custom voice upload")
