import cv2
import mediapipe as mp
import numpy as np

class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.landmark_indices = {
            'WRIST': 0,
            'THUMB_CMC': 1,
            'THUMB_MCP': 2,
            'THUMB_IP': 3,
            'THUMB_TIP': 4,
            'INDEX_FINGER_MCP': 5,
            'INDEX_FINGER_PIP': 6,
            'INDEX_FINGER_DIP': 7,
            'INDEX_FINGER_TIP': 8,
            'MIDDLE_FINGER_MCP': 9,
            'MIDDLE_FINGER_PIP': 10,
            'MIDDLE_FINGER_DIP': 11,
            'MIDDLE_FINGER_TIP': 12,
            'RING_FINGER_MCP': 13,
            'RING_FINGER_PIP': 14,
            'RING_FINGER_DIP': 15,
            'RING_FINGER_TIP': 16,
            'PINKY_MCP': 17,
            'PINKY_PIP': 18,
            'PINKY_DIP': 19,
            'PINKY_TIP': 20
        }
        
    def find_hands(self, img, draw=True):
        """
        Detect hands in an image and optionally draw landmarks
        
        Args:
            img: Input RGB image
            draw: Whether to draw hand landmarks on the image
            
        Returns:
            img: Image with or without drawn landmarks
            results: MediaPipe hand detection results
        """
        # Convert to RGB as MediaPipe requires RGB input
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS
                    )
                    
        return img
    
    def find_positions(self, img, hand_no=0):
        """
        Find the positions of all landmarks for a specific hand
        
        Args:
            img: Input image
            hand_no: Index of the hand when multiple hands are detected
            
        Returns:
            landmark_list: List of landmark positions [id, x, y]
        """
        landmark_list = []
        img_height, img_width, _ = img.shape
        
        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) > hand_no:
                hand = self.results.multi_hand_landmarks[hand_no]
                
                for id, lm in enumerate(hand.landmark):
                    # Convert normalized coordinates to pixel coordinates
                    x, y = int(lm.x * img_width), int(lm.y * img_height)
                    landmark_list.append([id, x, y])
                    
        return landmark_list
    
    def get_landmark_name(self, landmark_id):
        """Get the name of a landmark by its ID"""
        for name, id in self.landmark_indices.items():
            if id == landmark_id:
                return name
        return None
    
    def get_landmark_id(self, landmark_name):
        """Get the ID of a landmark by its name"""
        return self.landmark_indices.get(landmark_name, None)
    
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return np.sqrt((point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)
