import cv2
import numpy as np
import time
import argparse
import os
import sys

# Check for MediaPipe availability
mediapipe_available = True
try:
    import mediapipe as mp
except ImportError:
    mediapipe_available = False
    print("WARNING: MediaPipe is not installed. Using fallback mode with limited functionality.")
    print("For full functionality, please install MediaPipe.")

# Import our modules
from utils.laptop_controller import LaptopController
from utils.gesture_recognizer import GestureRecognizer
# Conditionally import modules that depend on MediaPipe
if mediapipe_available:
    from utils.hand_detector import HandDetector
    from utils.gesture_mapper import GestureMapper

def fallback_mode(args):
    """Run in fallback mode when MediaPipe is not available"""
    print("\nRunning in FALLBACK MODE (MediaPipe not available)")
    print("---------------------------------------------------")
    print("In this mode, you can only test basic camera functionality.")
    print("For full gesture control, please install MediaPipe.")
    
    # Initialize webcam
    cap = cv2.VideoCapture(args.camera)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    # Frame rate calculation variables
    prev_frame_time = 0
    curr_frame_time = 0
    fps = 0
    
    print("\nPress 'q' to exit")
    
    while True:
        # Read frame from webcam
        success, img = cap.read()
        if not success:
            print("Failed to capture image from webcam")
            break
            
        # Flip the image horizontally if requested
        if args.flip:
            img = cv2.flip(img, 1)
            
        # Calculate FPS
        if args.show_fps:
            curr_frame_time = time.time()
            fps = 1 / (curr_frame_time - prev_frame_time) if (curr_frame_time - prev_frame_time) > 0 else 0
            prev_frame_time = curr_frame_time
            
            # Display FPS
            cv2.putText(img, f"FPS: {int(fps)}", (10, 30), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display info text
        cv2.putText(img, "FALLBACK MODE - MediaPipe not available", (10, 60), 
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(img, "Install MediaPipe for gesture recognition", (10, 90), 
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Display the frame
        cv2.imshow("Camera Test (Fallback Mode)", img)
        
        # Check for key presses
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

def main():
    parser = argparse.ArgumentParser(description='AI-based Hand Gesture Control System')
    parser.add_argument('--model', type=str, default='models/gesture_model.pkl', 
                        help='Path to trained gesture model')
    parser.add_argument('--camera', type=int, default=0, 
                        help='Camera index (default: 0)')
    parser.add_argument('--flip', action='store_true', 
                        help='Flip camera horizontally')
    parser.add_argument('--show-fps', action='store_true', 
                        help='Display FPS on screen')
    parser.add_argument('--debug', action='store_true', 
                        help='Show debug information')
    parser.add_argument('--fallback', action='store_true', 
                        help='Force fallback mode (no MediaPipe)')
    args = parser.parse_args()
    
    # If MediaPipe is not available or fallback mode is requested, run in fallback mode
    if args.fallback or not mediapipe_available:
        fallback_mode(args)
        return
    
    # Check if model exists
    if not os.path.exists(args.model):
        print(f"Model file not found: {args.model}")
        print("Creating a placeholder model...")
        try:
            from sklearn.ensemble import RandomForestClassifier
            model = RandomForestClassifier(n_estimators=10, random_state=42)
            X = np.random.rand(100, 42)
            y = np.random.randint(0, 8, 100)
            model.fit(X, y)
            os.makedirs(os.path.dirname(args.model), exist_ok=True)
            import pickle
            with open(args.model, 'wb') as f:
                pickle.dump(model, f)
            print(f"Created placeholder model at {args.model}")
        except Exception as e:
            print(f"Error creating placeholder model: {e}")
            print("You need to train a model first. Run collect_data.py and then train_model.py.")
            return
    
    # Initialize components
    try:
        detector = HandDetector(detection_confidence=0.7, tracking_confidence=0.7)
        recognizer = GestureRecognizer(model_path=args.model)
        laptop_controller = LaptopController()
        gesture_mapper = GestureMapper(laptop_controller)
    except Exception as e:
        print(f"Error initializing components: {e}")
        print("Falling back to basic mode...")
        fallback_mode(args)
        return
    
    # Initialize webcam
    cap = cv2.VideoCapture(args.camera)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    # Frame rate calculation variables
    prev_frame_time = 0
    curr_frame_time = 0
    fps = 0
    
    print("\nAI-based Hand Gesture Control System")
    print("-----------------------------------")
    print("Press 'q' to exit")
    print("Press 'd' to toggle debug mode")
    print("\nAvailable gestures:")
    print("- Point: Move cursor")
    print("- Fist: Click")
    print("- Open palm: Scroll")
    print("- Victory sign: Right click")
    print("- Thumbs up: Volume up")
    print("- Pinch: Drag items")
    print("- Swipe left/right: Navigate back/forward")
    
    show_debug = args.debug
    
    while True:
        try:
            # Read frame from webcam
            success, img = cap.read()
            if not success:
                print("Failed to capture image from webcam")
                break
                
            # Flip the image horizontally if requested
            if args.flip:
                img = cv2.flip(img, 1)
                
            # Find hands in the frame
            img = detector.find_hands(img)
            
            # Find positions of landmarks
            landmark_list = detector.find_positions(img)
            
            # Calculate FPS
            if args.show_fps:
                curr_frame_time = time.time()
                fps = 1 / (curr_frame_time - prev_frame_time) if (curr_frame_time - prev_frame_time) > 0 else 0
                prev_frame_time = curr_frame_time
                
                # Display FPS
                cv2.putText(img, f"FPS: {int(fps)}", (10, 30), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Recognize gesture if hand is detected
            if landmark_list:
                # Predict gesture
                gesture, confidence = recognizer.predict(landmark_list)
                
                # Map gesture to action
                gesture_mapper.map_gesture_to_action(gesture, landmark_list, confidence)
                
                # Display gesture and confidence in debug mode
                if show_debug:
                    cv2.putText(img, f"Gesture: {gesture}", (10, 60), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.putText(img, f"Confidence: {confidence:.2f}", (10, 90), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            # Display the frame in debug mode
            if show_debug:
                cv2.imshow("Hand Gesture Control", img)
            
            # Check for key presses
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('d'):
                show_debug = not show_debug
                if not show_debug:
                    cv2.destroyAllWindows()
                    
        except Exception as e:
            print(f"Error during operation: {e}")
            print("Exiting...")
            break
            
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
