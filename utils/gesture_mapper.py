import numpy as np
import time

class GestureMapper:
    def __init__(self, laptop_controller):
        """
        Initialize the gesture mapper
        
        Args:
            laptop_controller: Instance of LaptopController
        """
        self.controller = laptop_controller
        
        # Track last gesture for continuous actions
        self.last_gesture = None
        self.last_gesture_time = time.time()
        
        # Gesture history for gesture sequences and motion detection
        self.gesture_history = []
        self.position_history = []
        
        # Maximum history length to maintain
        self.max_history_length = 10
        
        # Minimum time before a gesture can be repeated (seconds)
        self.gesture_cooldown = 0.5
        
        # For tracking movement during gestures
        self.tracking_start_position = None
        self.is_tracking_motion = False
        
    def map_gesture_to_action(self, gesture, landmarks, confidence):
        """
        Maps a recognized gesture to a laptop control action
        
        Args:
            gesture: Recognized gesture name
            landmarks: List of hand landmark positions
            confidence: Confidence score of the gesture recognition
        """
        # Only process gestures with sufficient confidence
        if confidence < 0.6:
            return
            
        current_time = time.time()
        
        # Add to gesture history
        self.gesture_history.append((gesture, current_time))
        if len(self.gesture_history) > self.max_history_length:
            self.gesture_history.pop(0)
            
        # If landmarks exist, add index finger position to position history
        if landmarks and len(landmarks) > 8:  # Ensure index finger tip exists
            index_finger_tip = landmarks[8]  # Index finger tip
            self.position_history.append((index_finger_tip[1], index_finger_tip[2], current_time))
            if len(self.position_history) > self.max_history_length:
                self.position_history.pop(0)
            
        # Check for cooldown on repeated gestures
        if gesture == self.last_gesture and (current_time - self.last_gesture_time) < self.gesture_cooldown:
            return
            
        self.last_gesture = gesture
        self.last_gesture_time = current_time
        
        # Map gestures to actions
        if gesture == "point":
            self._handle_point_gesture(landmarks)
        elif gesture == "fist":
            self._handle_fist_gesture()
        elif gesture == "open_palm":
            self._handle_open_palm_gesture(landmarks)
        elif gesture == "victory":
            self._handle_victory_gesture(landmarks)
        elif gesture == "thumb_up":
            self._handle_thumb_up_gesture()
        elif gesture == "pinch":
            self._handle_pinch_gesture(landmarks)
        elif gesture == "swipe_left":
            self._handle_swipe_left_gesture()
        elif gesture == "swipe_right":
            self._handle_swipe_right_gesture()
            
    def _handle_point_gesture(self, landmarks):
        """Handle pointing gesture - move cursor"""
        if not landmarks or len(landmarks) < 9:
            return
            
        # Use index finger tip for cursor position
        index_finger_tip = landmarks[8]  # Index finger tip
        
        # Get screen dimensions
        screen_width, screen_height = self.controller.screen_width, self.controller.screen_height
        
        # Calculate normalized position (accounting for camera flip)
        x_normalized = 1.0 - (index_finger_tip[1] / 640)  # Assuming 640x480 camera
        y_normalized = index_finger_tip[2] / 480
        
        # Move mouse to the position
        self.controller.move_mouse(x_normalized, y_normalized)
        
    def _handle_fist_gesture(self):
        """Handle fist gesture - mouse click"""
        self.controller.click(button='left')
        
    def _handle_open_palm_gesture(self, landmarks):
        """Handle open palm gesture - scroll"""
        if not landmarks or len(landmarks) < 9:
            return
            
        # Use palm position (middle point) for scroll direction
        wrist = landmarks[0]  # Wrist
        middle_finger_mcp = landmarks[9]  # Middle finger MCP
        
        # Calculate palm position
        palm_y = (wrist[2] + middle_finger_mcp[2]) / 2
        
        # Check if we have previous positions to compare
        if self.position_history and len(self.position_history) > 2:
            prev_pos = self.position_history[-2]
            prev_y = prev_pos[1]  # y-coordinate
            
            # Determine scroll direction based on hand movement
            if abs(palm_y - prev_y) > 10:  # Threshold to avoid small movements
                if palm_y < prev_y:
                    self.controller.scroll('up')
                else:
                    self.controller.scroll('down')
                    
    def _handle_victory_gesture(self, landmarks):
        """Handle victory sign gesture - right click"""
        self.controller.right_click()
        
    def _handle_thumb_up_gesture(self):
        """Handle thumbs up gesture - increase volume"""
        self.controller.adjust_volume('up')
        
    def _handle_pinch_gesture(self, landmarks):
        """
        Handle pinch gesture
        - If started with open fingers, track as a drag operation
        - If started with closed fingers, adjust volume
        """
        if not landmarks or len(landmarks) < 9:
            return
            
        # Use index finger tip for position
        index_finger_tip = landmarks[8]
        thumb_tip = landmarks[4]
        
        # Calculate distance between thumb and index finger
        dx = thumb_tip[1] - index_finger_tip[1]
        dy = thumb_tip[2] - index_finger_tip[2]
        distance = np.sqrt(dx*dx + dy*dy)
        
        # If the distance is small, it's a pinch
        if distance < 30:  # Threshold for pinch
            # Calculate normalized position
            x_normalized = 1.0 - (index_finger_tip[1] / 640)
            y_normalized = index_finger_tip[2] / 480
            
            # Perform drag operation
            self.controller.drag(x_normalized, y_normalized)
            
    def _handle_swipe_left_gesture(self):
        """Handle swipe left gesture - previous track/page"""
        # Check for quick left motion in position history
        self._detect_swipe('left')
        
    def _handle_swipe_right_gesture(self):
        """Handle swipe right gesture - next track/page"""
        # Check for quick right motion in position history
        self._detect_swipe('right')
        
    def _detect_swipe(self, direction):
        """
        Detect a swipe gesture based on position history
        
        Args:
            direction: 'left' or 'right'
        """
        if len(self.position_history) < 3:
            return False
            
        # Get the recent positions
        recent_positions = self.position_history[-3:]
        
        # Calculate horizontal movement
        start_x = recent_positions[0][0]
        end_x = recent_positions[-1][0]
        time_diff = recent_positions[-1][2] - recent_positions[0][2]
        
        # Calculate speed of movement
        if time_diff > 0:
            speed = abs(end_x - start_x) / time_diff
            
            # Check if movement is significant and in the right direction
            if speed > 300:  # Pixels per second threshold
                if direction == 'left' and end_x < start_x:
                    self.controller.key_combination(['alt', 'left'])
                    return True
                elif direction == 'right' and end_x > start_x:
                    self.controller.key_combination(['alt', 'right'])
                    return True
                    
        return False
