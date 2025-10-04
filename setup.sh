#!/bin/bash

# AI Gesture Control System - Easy Setup Script
echo "========================================"
echo "  AI Gesture Control System Setup"
echo "========================================"

# Check if Python is installed
if command -v python3 &>/dev/null; then
    echo "✅ Python 3 is installed"
else
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    echo "   Visit https://www.python.org/downloads/ to download Python."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    echo "❌ Python version $PYTHON_VERSION is not supported."
    echo "   Please install Python 3.7 or higher."
    exit 1
else
    echo "✅ Python version $PYTHON_VERSION is supported"
fi

# Create virtual environment
echo -e "\n📦 Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment."
    exit 1
fi

# Activate virtual environment
echo -e "\n🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo -e "\n🔄 Upgrading pip..."
pip install --upgrade pip

# Install packages individually to better handle errors
echo -e "\n📚 Installing required packages..."

# Install numpy first (as it's a dependency for many packages)
echo "Installing numpy..."
pip install "numpy>=1.24.0"

# Install OpenCV
echo "Installing OpenCV..."
pip install "opencv-python>=4.8.0"

# Install MediaPipe (with error handling for Apple Silicon)
echo "Installing MediaPipe..."
pip install "mediapipe>=0.9.0" || {
    echo "⚠️ MediaPipe installation failed. Trying alternative source..."
    # For Apple Silicon Macs, we might need a specific version
    pip install mediapipe-silicon || echo "⚠️ MediaPipe installation failed. Some features may not work."
}

# Install tensorflow (with special handling for Apple Silicon)
echo "Installing TensorFlow..."
if [ "$(uname -m)" = "arm64" ] && [ "$(uname)" = "Darwin" ]; then
    echo "Detected Apple Silicon Mac, installing tensorflow-macos..."
    pip install "tensorflow-macos>=2.12.0" || echo "⚠️ TensorFlow installation failed. Some features may not work."
else
    pip install "tensorflow>=2.12.0" || echo "⚠️ TensorFlow installation failed. Some features may not work."
fi

# Install other dependencies
echo "Installing other dependencies..."
pip install "scikit-learn>=1.0.0" "pyautogui>=0.9.54" "gdown>=4.6.0" || echo "⚠️ Some dependencies failed to install."

# Create directories
echo -e "\n📁 Creating necessary directories..."
mkdir -p data/gestures
mkdir -p models

# Download pretrained model
echo -e "\n🧠 Setting up pretrained model..."
python download_model.py || {
    echo "⚠️ Failed to download model. Creating a placeholder model instead..."
    python -c "
import os, pickle, numpy as np
from sklearn.ensemble import RandomForestClassifier
print('Creating a simple placeholder model...')
os.makedirs('models', exist_ok=True)
model = RandomForestClassifier(n_estimators=10, random_state=42)
X = np.random.rand(100, 42)
y = np.random.randint(0, 8, 100)
model.fit(X, y)
with open('models/gesture_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print('Created placeholder model at models/gesture_model.pkl')
"
}

echo -e "\n✨ Setup complete! ✨"
echo "========================================"
echo "To start the application, run:"
echo "./run.sh"
echo "or"
echo "source venv/bin/activate"
echo "python main.py"
echo "========================================"
