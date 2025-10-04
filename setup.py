#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        return False
    return True

def install_requirements():
    """Install required packages"""
    print("\n=== Installing required packages ===")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to install required packages.")
        return False

def download_model():
    """Download the pretrained model"""
    print("\n=== Downloading pretrained model ===")
    try:
        subprocess.check_call([sys.executable, "download_model.py"])
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to download pretrained model.")
        return False

def check_camera():
    """Check if camera is available"""
    print("\n=== Checking camera availability ===")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Warning: Could not access the camera.")
            print("Make sure your camera is connected and not being used by another application.")
            return False
        else:
            cap.release()
            print("Camera is available.")
            return True
    except:
        print("Warning: Could not check camera. OpenCV might not be installed correctly.")
        return False

def create_data_folders():
    """Create necessary data folders"""
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/gestures", exist_ok=True)
    os.makedirs("models", exist_ok=True)

def main():
    """Main setup function"""
    print("===================================")
    print("AI Gesture Control System - Setup")
    print("===================================")
    
    # Check Python version
    if not check_python_version():
        return
    
    # Create necessary folders
    create_data_folders()
    
    # Install requirements
    if not install_requirements():
        print("\nWarning: Some packages may not have been installed correctly.")
        input("Press Enter to continue anyway...")
    
    # Download pretrained model
    if not download_model():
        print("\nWarning: Could not download the pretrained model.")
        print("The application may not work correctly.")
        input("Press Enter to continue anyway...")
    
    # Check camera
    check_camera()
    
    print("\n===================================")
    print("Setup complete!")
    print("To run the application, use:")
    print("python main.py")
    print("===================================")

if __name__ == "__main__":
    main()
