import cv2
import numpy as np
import os
import time
from utils.hand_detector import HandDetector
import argparse

def collect_gesture_data():
    """Collect training data for hand gesture recognition"""
    parser = argparse.ArgumentParser(description='Collect hand gesture training data')
    parser.add_argument('--gesture', type=str, required=True, help='Name of the gesture to collect')
    parser.add_argument('--samples', type=int, default=200, help='Number of samples to collect')
    parser.add_argument('--output', type=str, default='data/gestures', help='Output directory')
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    gesture_dir = os.path.join(args.output, args.gesture)
    os.makedirs(gesture_dir, exist_ok=True)
    
    # Initialize hand detector
    detector = HandDetector(detection_confidence=0.7)
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    # Counter for samples
    counter = 0
    
    # Delay before starting collection
    delay_seconds = 5
    start_time = time.time()
    collecting = False
    
    print(f"Preparing to collect {args.samples} samples for gesture '{args.gesture}'")
    print(f"Get ready! Collection will start in {delay_seconds} seconds...")
    
    while True:
        # Read frame from webcam
        success, img = cap.read()
        if not success:
            print("Failed to capture image from webcam")
            break
            
        # Flip the image horizontally for a more intuitive experience
        img = cv2.flip(img, 1)
        
        # Find hands in the frame
        img = detector.find_hands(img)
        
        # Find positions of landmarks
        landmark_list = detector.find_positions(img)
        
        # Display countdown during delay
        elapsed = time.time() - start_time
        if not collecting and elapsed < delay_seconds:
            seconds_left = max(0, int(delay_seconds - elapsed))
            cv2.putText(img, f"Starting in: {seconds_left}", (20, 40),
                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif not collecting:
            collecting = True
            print("Started collecting samples...")
            
        # If collecting and hand is detected, save the landmark data
        if collecting and landmark_list:
            if counter < args.samples:
                # Prepare data to save
                data = np.array(landmark_list)
                # Save to file
                np.save(os.path.join(gesture_dir, f"sample_{counter:03d}"), data)
                counter += 1
                
                # Show progress
                cv2.putText(img, f"Collecting: {counter}/{args.samples}", (20, 40),
                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                          
                # Small delay between captures
                time.sleep(0.05)
            else:
                print(f"Finished collecting {args.samples} samples for gesture '{args.gesture}'")
                break
                
        # Draw a rectangle to indicate hand position area
        cv2.rectangle(img, (50, 50), (590, 430), (0, 255, 0), 2)
        
        # Display instructions
        cv2.putText(img, "Keep hand inside the box", (50, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
        cv2.putText(img, f"Collecting gesture: {args.gesture}", (50, 470),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
                  
        # Show the frame
        cv2.imshow("Data Collection", img)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    collect_gesture_data()
