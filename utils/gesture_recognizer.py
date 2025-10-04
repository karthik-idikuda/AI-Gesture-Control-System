import numpy as np
import pickle
import os

class GestureRecognizer:
    def __init__(self, model_path=None):
        """
        Initialize the gesture recognizer
        
        Args:
            model_path: Path to a pre-trained model file (optional)
        """
        self.model = None
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
            
        self.gestures = {
            0: "idle",
            1: "point",
            2: "fist",
            3: "open_palm",
            4: "victory",
            5: "thumb_up",
            6: "pinch",
            7: "swipe_left",
            8: "swipe_right"
        }
            
    def preprocess_landmarks(self, landmark_list):
        """
        Preprocess landmarks to create feature vector
        
        Args:
            landmark_list: List of landmark positions [id, x, y]
            
        Returns:
            features: Numpy array of processed features
        """
        if not landmark_list:
            return None
        
        # Extract x, y coordinates from the landmark list
        points = np.array([(lm[1], lm[2]) for lm in landmark_list])
        
        # Center the points by subtracting the mean
        centered = points - np.mean(points, axis=0)
        
        # Normalize to have max distance of 1.0
        if np.max(np.abs(centered)) > 0:
            centered = centered / np.max(np.abs(centered))
            
        # Flatten the coordinates into a feature vector
        features = centered.flatten()
        
        return features
    
    def predict(self, landmark_list):
        """
        Recognize gesture from landmark list
        
        Args:
            landmark_list: List of landmark positions [id, x, y]
            
        Returns:
            gesture: Predicted gesture name
            confidence: Prediction confidence
        """
        if not self.model or not landmark_list:
            return "unknown", 0.0
        
        features = self.preprocess_landmarks(landmark_list)
        if features is None:
            return "unknown", 0.0
        
        # Reshape for model input
        features = features.reshape(1, -1)
        
        # Make prediction
        try:
            prediction = self.model.predict(features)
            gesture_id = int(prediction[0])
            
            # Get prediction probabilities if available
            confidence = 0.0
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(features)
                confidence = float(np.max(probabilities))
                
            return self.gestures.get(gesture_id, "unknown"), confidence
        except:
            return "unknown", 0.0
    
    def save_model(self, model_path):
        """Save the trained model to disk"""
        if self.model:
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
                
    def load_model(self, model_path):
        """Load a trained model from disk"""
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
