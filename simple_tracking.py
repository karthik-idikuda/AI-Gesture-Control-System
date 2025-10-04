#!/usr/bin/env python3
import cv2
import numpy as np
import pyautogui
import time
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Simple Color-Based Hand Tracking')
    parser.add_argument('--camera', type=int, default=0, help='Camera index (default: 0)')
    parser.add_argument('--flip', action='store_true', help='Flip camera horizontally')
    parser.add_argument('--show-fps', action='store_true', help='Display FPS on screen')
    args = parser.parse_args()
    
    # Get screen dimensions
    screen_width, screen_height = pyautogui.size()
    
    # Initialize webcam
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    # Get webcam dimensions
    _, frame = cap.read()
    frame_height, frame_width = frame.shape[0], frame.shape[1]
    
    # Frame rate calculation variables
    prev_frame_time = 0
    curr_frame_time = 0
    fps = 0
    
    # For clicking functionality
    last_click_time = 0
    click_cooldown = 1.0  # seconds
    
    # Create trackbars to adjust HSV range
    cv2.namedWindow('Controls')
    cv2.createTrackbar('Hue Low', 'Controls', 0, 179, lambda x: None)
    cv2.createTrackbar('Hue High', 'Controls', 25, 179, lambda x: None)
    cv2.createTrackbar('Sat Low', 'Controls', 50, 255, lambda x: None)
    cv2.createTrackbar('Sat High', 'Controls', 255, 255, lambda x: None)
    cv2.createTrackbar('Val Low', 'Controls', 50, 255, lambda x: None)
    cv2.createTrackbar('Val High', 'Controls', 255, 255, lambda x: None)
    
    # Set initial values (skin color range)
    cv2.setTrackbarPos('Hue Low', 'Controls', 0)
    cv2.setTrackbarPos('Hue High', 'Controls', 25)
    cv2.setTrackbarPos('Sat Low', 'Controls', 50)
    cv2.setTrackbarPos('Sat High', 'Controls', 255)
    cv2.setTrackbarPos('Val Low', 'Controls', 50)
    cv2.setTrackbarPos('Val High', 'Controls', 255)
    
    print("\nSimple Color-Based Hand Tracking")
    print("-------------------------------")
    print("Adjust the trackbars to detect your skin tone.")
    print("Hold your hand in front of the camera to control the cursor.")
    print("Make a fist and hold it still for 1 second to click.")
    print("Press 'q' to exit.")
    
    while True:
        # Read frame from webcam
        success, frame = cap.read()
        if not success:
            print("Failed to capture image from webcam")
            break
            
        # Flip the image horizontally if requested
        if args.flip:
            frame = cv2.flip(frame, 1)
        
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Get current trackbar values
        h_low = cv2.getTrackbarPos('Hue Low', 'Controls')
        h_high = cv2.getTrackbarPos('Hue High', 'Controls')
        s_low = cv2.getTrackbarPos('Sat Low', 'Controls')
        s_high = cv2.getTrackbarPos('Sat High', 'Controls')
        v_low = cv2.getTrackbarPos('Val Low', 'Controls')
        v_high = cv2.getTrackbarPos('Val High', 'Controls')
        
        # Create a mask for skin color
        lower = np.array([h_low, s_low, v_low])
        upper = np.array([h_high, s_high, v_high])
        mask = cv2.inRange(hsv, lower, upper)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find the largest contour (assuming it's the hand)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            # Only process if the contour is large enough (to avoid noise)
            if area > 3000:
                # Get the bounding rectangle
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Calculate the centroid
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    
                    # Draw centroid
                    cv2.circle(frame, (cx, cy), 7, (0, 0, 255), -1)
                    
                    # Map the position to screen coordinates
                    screen_x = int((cx / frame_width) * screen_width)
                    screen_y = int((cy / frame_height) * screen_height)
                    
                    # Move the mouse cursor
                    pyautogui.moveTo(screen_x, screen_y)
                    
                    # Calculate hand aspect ratio - can be used to detect gestures
                    aspect_ratio = float(h) / w if w > 0 else 0
                    
                    # If aspect ratio is close to 1, it might be a fist (for clicking)
                    if 0.8 < aspect_ratio < 1.2:
                        cv2.putText(frame, "Fist detected", (10, 60), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                        
                        # Click after holding for a moment (avoid accidental clicks)
                        current_time = time.time()
                        if current_time - last_click_time > click_cooldown:
                            pyautogui.click()
                            last_click_time = current_time
                    else:
                        cv2.putText(frame, "Hand detected", (10, 60), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Calculate FPS
        if args.show_fps:
            curr_frame_time = time.time()
            fps = 1 / (curr_frame_time - prev_frame_time) if (curr_frame_time - prev_frame_time) > 0 else 0
            prev_frame_time = curr_frame_time
            
            # Display FPS
            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show the original frame and mask
        cv2.imshow('Hand Tracking', frame)
        cv2.imshow('Mask', mask)
        
        # Check for key presses
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
