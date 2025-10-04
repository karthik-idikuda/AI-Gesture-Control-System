#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found."
    echo "   Please run './setup.sh' first to set up the project."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Ensure necessary directories exist
mkdir -p data/gestures
mkdir -p models

# Check if the model exists
if [ ! -f "models/gesture_model.pkl" ]; then
    echo "⚠️ Model file not found, creating one now..."
    python -c "
import os, pickle, numpy as np
from sklearn.ensemble import RandomForestClassifier
print('Creating a simple placeholder model...')
model = RandomForestClassifier(n_estimators=10, random_state=42)
X = np.random.rand(100, 42)
y = np.random.randint(0, 8, 100)
model.fit(X, y)
with open('models/gesture_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print('Created placeholder model at models/gesture_model.pkl')
"
fi

# Check if all required packages are installed
echo "Checking required packages..."
python -c "
import sys
missing = []
try:
    import cv2
except ImportError:
    missing.append('opencv-python')
try:
    import mediapipe
except ImportError:
    missing.append('mediapipe')
try:
    import numpy
except ImportError:
    missing.append('numpy')
try:
    import pyautogui
except ImportError:
    missing.append('pyautogui')
try:
    import sklearn
except ImportError:
    missing.append('scikit-learn')
    
if missing:
    print(f'Missing packages: {missing}')
    sys.exit(1)
else:
    print('All required packages are installed!')
    sys.exit(0)
"

if [ $? -ne 0 ]; then
    echo "⚠️ Some required packages are missing. Attempting to install them..."
    pip install opencv-python numpy pyautogui scikit-learn
    pip install mediapipe || pip install mediapipe-silicon || echo "⚠️ Could not install MediaPipe. Some features may not work."
fi

# Run the main application
echo "🚀 Starting AI Gesture Control System..."
python main.py --debug

# Deactivate virtual environment when done
deactivate
