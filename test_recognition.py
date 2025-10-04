import cv2
import time
import os
from utils.hand_detector import HandDetector
from utils.gesture_recognizer import GestureRecognizer

def test_gesture_recognition():
    """Test the gesture recognition with the pretrained model"""
    print("\n=== Testing Gesture Recognition ===")
    
    # Check if model exists
    model_path = 'models/gesture_model.pkl'
    if not os.path.exists(model_path):
        print(f"Model file not found: {model_path}")
        print("Please run setup.py first to download the pretrained model.")
        return
    
    # Initialize components
    detector = HandDetector(detection_confidence=0.7)
    recognizer = GestureRecognizer(model_path=model_path)
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    print("\nGesture Recognition Test")
    print("-----------------------")
    print("Show different hand gestures to the camera.")
    print("The recognized gesture will be displayed.")
    print("Press 'q' to exit")
    
    start_time = time.time()
    frame_count = 0
    
    while True:
        # Read frame from webcam
        success, img = cap.read()
        if not success:
            print("Failed to capture image from webcam")
            break
            
        # Flip the image horizontally for more intuitive interaction
        img = cv2.flip(img, 1)
        
        # Find hands in the frame
        img = detector.find_hands(img)
        
        # Find positions of landmarks
        landmark_list = detector.find_positions(img)
        
        # Recognize gesture if hand is detected
        if landmark_list:
            # Predict gesture
            gesture, confidence = recognizer.predict(landmark_list)
            
            # Display gesture and confidence
            cv2.putText(img, f"Gesture: {gesture}", (10, 50), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, f"Confidence: {confidence:.2f}", (10, 90), 
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Calculate FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        
        # Display FPS
        cv2.putText(img, f"FPS: {int(fps)}", (10, 30), 
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Display the frame
        cv2.imshow("Gesture Recognition Test", img)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_gesture_recognition()
