#!/bin/bash

echo "========================================"
echo "DeLuxTTS OpenAI-Compatible API Server"
echo "========================================"
echo ""

cd /home/op/DeLuxTTS

echo "Checking Python environment..."
python --version

echo ""
echo "Checking dependencies..."
python -c "import fastapi; print('✓ FastAPI:', fastapi.__version__)" || echo "✗ FastAPI not installed"
python -c "import uvicorn; print('✓ Uvicorn:', uvicorn.__version__)" || echo "✗ Uvicorn not installed"
python -c "import torch; print('✓ PyTorch:', torch.__version__)" || echo "✗ PyTorch not installed"

echo ""
echo "Checking default voices..."
if [ -d "default_voices" ]; then
    voice_count=$(ls default_voices/*.wav 2>/dev/null | wc -l)
    echo "✓ Found $voice_count voice files in default_voices/"
else
    echo "✗ default_voices/ directory not found"
fi

echo ""
echo "Starting server on http://0.0.0.0:8000"
echo "Press Ctrl+C to stop"
echo ""

python server.py
