# AI-Based Gesture Control System

This project implements an AI-based gesture control system that allows you to control your laptop using hand gestures captured through your webcam. It includes a pretrained model so you can start using it immediately without training your own model.

## Features

- Control mouse cursor with finger movements
- Perform clicks, right-clicks, and dragging operations
- Scroll up/down with hand gestures
- Adjust volume and media playback
- Navigate between pages with swipe gestures

## Supported Gestures

- **Point**: Move the cursor (using index finger)
- **Fist**: Left click
- **Open Palm**: Scroll up/down
- **Victory Sign**: Right click
- **Thumb Up**: Increase volume
- **Pinch**: Drag items
- **Swipe Left/Right**: Navigate back/forward in browser

## Requirements

- Python 3.7+
- Webcam
- Required Python libraries (see `requirements.txt`)

## Quick Start

The easiest way to get started is to use our automated setup script:

```bash
python setup.py
```

This will:
1. Install all required dependencies
2. Download the pretrained model
3. Set up the necessary directories

After setup is complete, run the main application:

```bash
python main.py
```

## Test the Recognition

To test if the gesture recognition is working properly before using it to control your laptop:

```bash
python test_recognition.py
```

This will open your webcam and show the recognized gestures in real-time.

## Usage

Start the gesture control system:

```bash
python main.py
```

Optional arguments:
- `--model`: Path to the trained model file (default: models/gesture_model.pkl)
- `--camera`: Camera index (default: 0)
- `--flip`: Flip camera horizontally
- `--show-fps`: Display FPS on screen
- `--debug`: Show debug information

Example:
```bash
python main.py --debug --show-fps
```

While running:
- Press 'd' to toggle debug mode (shows camera feed and recognized gestures)
- Press 'q' to quit

## Project Structure

- `main.py`: Main application script
- `setup.py`: Automated setup script to install dependencies and download the model
- `download_model.py`: Script to download the pretrained model
- `test_recognition.py`: Script to test gesture recognition
- `collect_data.py`: Script for collecting your own gesture training data (optional)
- `train_model.py`: Script for training your own model (optional)
- `utils/`: Utility modules
  - `hand_detector.py`: Hand detection using MediaPipe
  - `gesture_recognizer.py`: Gesture recognition
  - `laptop_controller.py`: Control laptop with gestures
  - `gesture_mapper.py`: Map gestures to actions

## Advanced Usage (Optional)

If you want to create your own custom model instead of using the pretrained one:

### 1. Data Collection

```bash
python collect_data.py --gesture point --samples 200
# Repeat for all gestures: fist, open_palm, victory, thumb_up, pinch, swipe_left, swipe_right, idle
```

### 2. Train Your Custom Model

```bash
python train_model.py
```

## Customization

You can modify the `gesture_mapper.py` file to customize how gestures are mapped to actions according to your preferences.

## Troubleshooting

- **Camera not detected**: Make sure your webcam is properly connected and not being used by another application
- **Poor recognition**: Try adjusting lighting conditions or camera position
- **Model download fails**: Check your internet connection or try running `download_model.py` separately
- **Lag or slow performance**: Lower the webcam resolution or close other resource-intensive applications

## Limitations

- Recognition accuracy depends on lighting conditions and webcam quality
- Some gestures might be misclassified if they look similar
- System control capabilities may vary by operating system

## License

This project is available for personal use.
# AI---Gesture-Control-
