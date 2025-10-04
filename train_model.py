import os
import numpy as np
import glob
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from utils.gesture_recognizer import GestureRecognizer
import argparse

def preprocess_data(data_dir):
    """
    Preprocess gesture data for training
    
    Args:
        data_dir: Directory containing gesture data
        
    Returns:
        X: Features
        y: Labels
    """
    X = []
    y = []
    
    # Get all gesture folders
    gesture_folders = [os.path.join(data_dir, d) for d in os.listdir(data_dir) 
                      if os.path.isdir(os.path.join(data_dir, d))]
    
    # Create a gesture recognizer for preprocessing
    recognizer = GestureRecognizer()
    
    # Define gesture mapping
    gesture_mapping = {
        "idle": 0,
        "point": 1,
        "fist": 2,
        "open_palm": 3,
        "victory": 4,
        "thumb_up": 5,
        "pinch": 6,
        "swipe_left": 7,
        "swipe_right": 8
    }
    
    print("Loading gesture data...")
    for gesture_folder in gesture_folders:
        gesture_name = os.path.basename(gesture_folder)
        
        if gesture_name not in gesture_mapping:
            print(f"Warning: Unknown gesture '{gesture_name}'. Skipping.")
            continue
            
        gesture_id = gesture_mapping[gesture_name]
        
        # Find all sample files for this gesture
        sample_files = glob.glob(os.path.join(gesture_folder, "sample_*.npy"))
        
        print(f"Found {len(sample_files)} samples for gesture '{gesture_name}'")
        
        for sample_file in sample_files:
            try:
                # Load landmark data
                landmarks = np.load(sample_file)
                
                # Preprocess landmarks to features
                features = recognizer.preprocess_landmarks(landmarks)
                
                if features is not None:
                    X.append(features)
                    y.append(gesture_id)
            except Exception as e:
                print(f"Error processing {sample_file}: {e}")
                
    return np.array(X), np.array(y)

def train_model():
    """Train a gesture recognition model"""
    parser = argparse.ArgumentParser(description='Train hand gesture recognition model')
    parser.add_argument('--data', type=str, default='data/gestures', help='Data directory')
    parser.add_argument('--output', type=str, default='models/gesture_model.pkl', help='Output model file')
    parser.add_argument('--test-size', type=float, default=0.2, help='Test set size (proportion)')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Load and preprocess data
    X, y = preprocess_data(args.data)
    
    if len(X) == 0:
        print("No training data found. Please run collect_data.py first.")
        return
        
    print(f"Loaded {len(X)} samples with {len(np.unique(y))} gestures")
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=42)
    
    # Train a Random Forest classifier
    print("Training model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred))
    
    # Create a gesture recognizer and save the model
    recognizer = GestureRecognizer()
    recognizer.model = model
    recognizer.save_model(args.output)
    
    print(f"Model saved to {args.output}")
    
if __name__ == "__main__":
    train_model()
