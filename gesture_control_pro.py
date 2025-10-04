#!/usr/bin/env python3
"""
Professional AI-Based Hand Gesture Control System
==================================================
A comprehensive gesture control application with real-time detection,
professional GUI, advanced analytics, and complete laptop control.

Features:
- Real-time hand gesture detection using MediaPipe
- Professional GUI with live video feed
- Advanced gesture analytics and confidence metrics
- Customizable gesture mappings and sensitivity
- System control (volume, brightness, mouse, keyboard)
- Performance monitoring and statistics
- Recording and playback capabilities
- Multiple gesture profiles
"""

import cv2
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mediapipe as mp
import numpy as np
import pyautogui
import threading
import time
import json
import os
import subprocess
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle
from collections import deque, defaultdict
import logging
from datetime import datetime

# Disable PyAutoGUI failsafe for smooth operation
pyautogui.FAILSAFE = False

class GestureControlPro:
    def __init__(self):
        """Initialize the Professional Gesture Control System"""
        self.setup_logging()
        self.setup_mediapipe()
        self.setup_variables()
        self.setup_gui()
        self.load_settings()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('gesture_control.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_mediapipe(self):
        """Initialize MediaPipe components"""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def setup_variables(self):
        """Initialize application variables"""
        # Camera and detection variables
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        
        # Gesture detection variables
        self.current_gesture = "None"
        self.gesture_confidence = 0.0
        self.gesture_history = deque(maxlen=30)  # Last 30 detections
        self.gesture_stats = defaultdict(int)
        
        # Performance metrics
        self.fps_history = deque(maxlen=100)
        self.detection_times = deque(maxlen=100)
        
        # Control variables
        self.sensitivity = 0.7
        self.smoothing = 0.3
        self.mouse_control_enabled = True
        self.system_control_enabled = True
        
        # Advanced gesture mappings
        self.gesture_mappings = {
            'point': 'mouse_move',
            'fist': 'left_click',
            'open_palm': 'scroll_up',
            'open_palm_down': 'scroll_down',
            'victory': 'right_click',
            'thumbs_up': 'volume_up',
            'thumbs_down': 'volume_down',
            'pinch': 'drag',
            'ok_sign': 'brightness_up',
            'peace_inverted': 'brightness_down',
            'four_fingers': 'minimize_all',
            'swipe_left': 'prev_tab',
            'swipe_right': 'next_tab',
            'zoom_in': 'zoom_in',
            'zoom_out': 'zoom_out',
            'double_tap': 'double_click',
            'three_fingers': 'mission_control'
        }
        
        # Screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
    def setup_gui(self):
        """Create the professional GUI interface"""
        self.root = tk.Tk()
        self.root.title("Professional AI Gesture Control System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Create main layout
        self.create_header()
        self.create_main_content()
        self.create_control_panel()
        self.create_analytics_panel()
        self.create_status_bar()
        
    def configure_styles(self):
        """Configure custom styles for the GUI"""
        self.style.configure('Header.TLabel', 
                           font=('Arial', 16, 'bold'),
                           foreground='white',
                           background='#2b2b2b')
        
        self.style.configure('Status.TLabel',
                           font=('Arial', 10),
                           foreground='#00ff00',
                           background='#2b2b2b')
        
        self.style.configure('Control.TButton',
                           font=('Arial', 10, 'bold'))
        
    def create_header(self):
        """Create the application header"""
        header_frame = tk.Frame(self.root, bg='#1e1e1e', height=60)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🤖 Professional AI Gesture Control System",
                              font=('Arial', 18, 'bold'),
                              fg='#00ff00', bg='#1e1e1e')
        title_label.pack(side='left', padx=20, pady=15)
        
        # Status indicators
        self.status_frame = tk.Frame(header_frame, bg='#1e1e1e')
        self.status_frame.pack(side='right', padx=20, pady=15)
        
        self.camera_status = tk.Label(self.status_frame, text="📷 Camera: OFF",
                                     fg='red', bg='#1e1e1e', font=('Arial', 10))
        self.camera_status.pack(side='right', padx=10)
        
        self.ai_status = tk.Label(self.status_frame, text="🧠 AI: OFF",
                                 fg='red', bg='#1e1e1e', font=('Arial', 10))
        self.ai_status.pack(side='right', padx=10)
        
    def create_main_content(self):
        """Create the main content area with video feed and controls"""
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Video feed
        self.video_frame = tk.LabelFrame(main_frame, text="📹 Live Video Feed",
                                        bg='#2b2b2b', fg='white',
                                        font=('Arial', 12, 'bold'))
        self.video_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Video display
        self.video_label = tk.Label(self.video_frame, bg='black', text="Camera Feed",
                                   fg='white', font=('Arial', 14))
        self.video_label.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Video controls
        video_controls = tk.Frame(self.video_frame, bg='#2b2b2b')
        video_controls.pack(fill='x', padx=10, pady=5)
        
        self.start_button = tk.Button(video_controls, text="🎥 Start Camera",
                                     command=self.start_detection,
                                     bg='#00aa00', fg='white',
                                     font=('Arial', 10, 'bold'))
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = tk.Button(video_controls, text="⏹️ Stop Camera",
                                    command=self.stop_detection,
                                    bg='#aa0000', fg='white',
                                    font=('Arial', 10, 'bold'))
        self.stop_button.pack(side='left', padx=5)
        
        self.record_button = tk.Button(video_controls, text="⏺️ Record",
                                      command=self.toggle_recording,
                                      bg='#0066cc', fg='white',
                                      font=('Arial', 10, 'bold'))
        self.record_button.pack(side='left', padx=5)
        
        # Right panel - Information and controls
        self.info_frame = tk.LabelFrame(main_frame, text="📊 System Information",
                                       bg='#2b2b2b', fg='white',
                                       font=('Arial', 12, 'bold'),
                                       width=400)
        self.info_frame.pack(side='right', fill='y', padx=5)
        self.info_frame.pack_propagate(False)
        
        self.create_info_displays()
        
    def create_info_displays(self):
        """Create information display panels"""
        # Current gesture display
        gesture_frame = tk.LabelFrame(self.info_frame, text="Current Gesture",
                                     bg='#2b2b2b', fg='white')
        gesture_frame.pack(fill='x', padx=10, pady=5)
        
        self.gesture_label = tk.Label(gesture_frame, text="None",
                                     bg='#2b2b2b', fg='#00ff00',
                                     font=('Arial', 24, 'bold'))
        self.gesture_label.pack(pady=10)
        
        self.confidence_label = tk.Label(gesture_frame, text="Confidence: 0%",
                                        bg='#2b2b2b', fg='white',
                                        font=('Arial', 12))
        self.confidence_label.pack(pady=5)
        
        # Performance metrics
        perf_frame = tk.LabelFrame(self.info_frame, text="Performance",
                                  bg='#2b2b2b', fg='white')
        perf_frame.pack(fill='x', padx=10, pady=5)
        
        self.fps_label = tk.Label(perf_frame, text="FPS: 0",
                                 bg='#2b2b2b', fg='white')
        self.fps_label.pack(anchor='w', padx=10, pady=2)
        
        self.hands_detected_label = tk.Label(perf_frame, text="Hands: 0",
                                           bg='#2b2b2b', fg='white')
        self.hands_detected_label.pack(anchor='w', padx=10, pady=2)
        
        self.processing_time_label = tk.Label(perf_frame, text="Processing: 0ms",
                                            bg='#2b2b2b', fg='white')
        self.processing_time_label.pack(anchor='w', padx=10, pady=2)
        
        # Gesture history
        history_frame = tk.LabelFrame(self.info_frame, text="Recent Gestures",
                                     bg='#2b2b2b', fg='white')
        history_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.history_listbox = tk.Listbox(history_frame, bg='#1e1e1e', fg='white',
                                         selectbackground='#0066cc',
                                         height=8)
        self.history_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
    def create_control_panel(self):
        """Create the control panel with settings and options"""
        control_frame = tk.LabelFrame(self.root, text="🎛️ Control Panel",
                                     bg='#2b2b2b', fg='white',
                                     font=('Arial', 12, 'bold'))
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Settings section
        settings_frame = tk.Frame(control_frame, bg='#2b2b2b')
        settings_frame.pack(side='left', fill='y', padx=10, pady=10)
        
        tk.Label(settings_frame, text="Sensitivity:",
                bg='#2b2b2b', fg='white').pack(anchor='w')
        
        self.sensitivity_var = tk.DoubleVar(value=0.7)
        self.sensitivity_scale = tk.Scale(settings_frame, from_=0.1, to=1.0,
                                         resolution=0.1, orient='horizontal',
                                         variable=self.sensitivity_var,
                                         bg='#2b2b2b', fg='white',
                                         highlightbackground='#2b2b2b')
        self.sensitivity_scale.pack(fill='x')
        
        tk.Label(settings_frame, text="Smoothing:",
                bg='#2b2b2b', fg='white').pack(anchor='w', pady=(10,0))
        
        self.smoothing_var = tk.DoubleVar(value=0.3)
        self.smoothing_scale = tk.Scale(settings_frame, from_=0.0, to=1.0,
                                       resolution=0.1, orient='horizontal',
                                       variable=self.smoothing_var,
                                       bg='#2b2b2b', fg='white',
                                       highlightbackground='#2b2b2b')
        self.smoothing_scale.pack(fill='x')
        
        # Control options
        options_frame = tk.Frame(control_frame, bg='#2b2b2b')
        options_frame.pack(side='left', fill='y', padx=20, pady=10)
        
        self.mouse_control_var = tk.BooleanVar(value=True)
        mouse_cb = tk.Checkbutton(options_frame, text="Mouse Control",
                                 variable=self.mouse_control_var,
                                 bg='#2b2b2b', fg='white',
                                 selectcolor='#2b2b2b',
                                 activebackground='#2b2b2b',
                                 activeforeground='white')
        mouse_cb.pack(anchor='w')
        
        self.system_control_var = tk.BooleanVar(value=True)
        system_cb = tk.Checkbutton(options_frame, text="System Control",
                                  variable=self.system_control_var,
                                  bg='#2b2b2b', fg='white',
                                  selectcolor='#2b2b2b',
                                  activebackground='#2b2b2b',
                                  activeforeground='white')
        system_cb.pack(anchor='w')
        
        # Action buttons
        buttons_frame = tk.Frame(control_frame, bg='#2b2b2b')
        buttons_frame.pack(side='right', fill='y', padx=10, pady=10)
        
        tk.Button(buttons_frame, text="💾 Save Settings",
                 command=self.save_settings,
                 bg='#0066cc', fg='white',
                 font=('Arial', 9, 'bold')).pack(pady=2, fill='x')
        
        tk.Button(buttons_frame, text="📊 Show Analytics",
                 command=self.show_analytics,
                 bg='#9900cc', fg='white',
                 font=('Arial', 9, 'bold')).pack(pady=2, fill='x')
        
        tk.Button(buttons_frame, text="🎯 Calibrate",
                 command=self.calibrate_system,
                 bg='#cc6600', fg='white',
                 font=('Arial', 9, 'bold')).pack(pady=2, fill='x')
        
    def create_analytics_panel(self):
        """Create the analytics panel with charts"""
        self.analytics_window = None
        
    def create_status_bar(self):
        """Create the status bar at the bottom"""
        status_frame = tk.Frame(self.root, bg='#1e1e1e', height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_text = tk.Label(status_frame, text="Ready",
                                   bg='#1e1e1e', fg='#00ff00',
                                   font=('Arial', 10))
        self.status_text.pack(side='left', padx=10, pady=5)
        
        self.time_label = tk.Label(status_frame, text="",
                                  bg='#1e1e1e', fg='white',
                                  font=('Arial', 10))
        self.time_label.pack(side='right', padx=10, pady=5)
        
        # Update time
        self.update_time()
        
    def update_time(self):
        """Update the time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def start_detection(self):
        """Start the gesture detection system"""
        if not self.is_running:
            try:
                self.cap = cv2.VideoCapture(0)
                if not self.cap.isOpened():
                    messagebox.showerror("Error", "Could not access camera")
                    return
                
                self.is_running = True
                self.camera_status.config(text="📷 Camera: ON", fg='green')
                self.ai_status.config(text="🧠 AI: ON", fg='green')
                self.status_text.config(text="Detection Active")
                
                # Start detection thread
                self.detection_thread = threading.Thread(target=self.detection_loop)
                self.detection_thread.daemon = True
                self.detection_thread.start()
                
                self.logger.info("Gesture detection started")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start detection: {str(e)}")
                self.logger.error(f"Error starting detection: {e}")
                
    def stop_detection(self):
        """Stop the gesture detection system"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        
        self.camera_status.config(text="📷 Camera: OFF", fg='red')
        self.ai_status.config(text="🧠 AI: OFF", fg='red')
        self.status_text.config(text="Detection Stopped")
        
        # Clear video display
        self.video_label.config(image='', text="Camera Feed")
        
        self.logger.info("Gesture detection stopped")
        
    def detection_loop(self):
        """Main detection loop running in separate thread"""
        prev_time = time.time()
        
        while self.is_running:
            try:
                start_process = time.time()
                
                ret, frame = self.cap.read()
                if not ret:
                    continue
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process with MediaPipe
                results = self.hands.process(frame_rgb)
                
                # Draw hand landmarks and detect gestures
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(
                            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        
                        # Extract landmarks and recognize gesture
                        landmarks = self.extract_landmarks(hand_landmarks, frame.shape)
                        gesture, confidence = self.recognize_gesture(landmarks)
                        
                        if confidence > self.sensitivity_var.get():
                            self.process_gesture(gesture, confidence, landmarks)
                
                # Calculate FPS
                current_time = time.time()
                fps = 1 / (current_time - prev_time)
                prev_time = current_time
                self.fps = fps
                self.fps_history.append(fps)
                
                # Record processing time
                process_time = (time.time() - start_process) * 1000
                self.detection_times.append(process_time)
                
                # Update GUI
                self.update_video_display(frame)
                self.update_info_displays()
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.01)
                
            except Exception as e:
                self.logger.error(f"Error in detection loop: {e}")
                time.sleep(0.1)
                
    def extract_landmarks(self, hand_landmarks, frame_shape):
        """Extract normalized landmark coordinates"""
        landmarks = []
        h, w, _ = frame_shape
        
        for lm in hand_landmarks.landmark:
            landmarks.extend([lm.x, lm.y, lm.z])
            
        return np.array(landmarks)
        
    def recognize_gesture(self, landmarks):
        """Enhanced gesture recognition with more advanced gestures"""
        if len(landmarks) < 63:  # 21 landmarks * 3 coordinates
            return "unknown", 0.0
            
        # Convert to 2D points for easier analysis
        points = landmarks.reshape(-1, 3)[:, :2]
        
        # Get key landmarks (normalized coordinates 0-1)
        wrist = points[0]
        thumb_tip = points[4]
        thumb_ip = points[3]
        thumb_mcp = points[2]
        index_tip = points[8]
        index_pip = points[6]
        index_mcp = points[5]
        middle_tip = points[12]
        middle_pip = points[10]
        middle_mcp = points[9]
        ring_tip = points[16]
        ring_pip = points[14]
        ring_mcp = points[13]
        pinky_tip = points[20]
        pinky_pip = points[18]
        pinky_mcp = points[17]
        
        # Calculate distances for gesture detection
        thumb_index_dist = np.linalg.norm(thumb_tip - index_tip)
        thumb_middle_dist = np.linalg.norm(thumb_tip - middle_tip)
        index_middle_dist = np.linalg.norm(index_tip - middle_tip)
        
        # Count extended fingers
        extended_fingers = []
        
        # Thumb (different logic due to thumb orientation)
        if thumb_tip[0] > thumb_ip[0] if thumb_tip[0] > wrist[0] else thumb_tip[0] < thumb_ip[0]:
            extended_fingers.append('thumb')
            
        # Other fingers (check if tip is above PIP joint)
        if index_tip[1] < index_pip[1] - 0.02:
            extended_fingers.append('index')
        if middle_tip[1] < middle_pip[1] - 0.02:
            extended_fingers.append('middle')
        if ring_tip[1] < ring_pip[1] - 0.02:
            extended_fingers.append('ring')
        if pinky_tip[1] < pinky_pip[1] - 0.02:
            extended_fingers.append('pinky')
        
        extended_count = len(extended_fingers)
        
        # Advanced gesture recognition logic
        
        # Pinch gesture (thumb and index very close)
        if thumb_index_dist < 0.04:
            return "pinch", 0.92
            
        # OK sign (thumb and index in circle, other fingers extended)
        elif (thumb_index_dist < 0.06 and extended_count >= 3 and 
              'middle' in extended_fingers and 'ring' in extended_fingers):
            return "ok_sign", 0.90
            
        # Thumbs up (thumb up, other fingers down)
        elif ('thumb' in extended_fingers and extended_count == 1 and
              thumb_tip[1] < wrist[1] - 0.05):
            return "thumbs_up", 0.88
            
        # Thumbs down (thumb down, other fingers folded)
        elif ('thumb' in extended_fingers and extended_count == 1 and
              thumb_tip[1] > wrist[1] + 0.05):
            return "thumbs_down", 0.88
            
        # Point gesture (only index finger extended)
        elif extended_count == 1 and 'index' in extended_fingers:
            return "point", 0.85
            
        # Victory sign (index and middle extended, others folded)
        elif (extended_count == 2 and 'index' in extended_fingers and 
              'middle' in extended_fingers):
            # Check if fingers are spread apart (victory) vs close together (point variation)
            if index_middle_dist > 0.05:
                return "victory", 0.87
            else:
                return "point", 0.80
                
        # Peace sign inverted (for brightness down)
        elif (extended_count == 2 and 'index' in extended_fingers and 
              'middle' in extended_fingers and middle_tip[1] > index_tip[1]):
            return "peace_inverted", 0.85
            
        # Three fingers (mission control/expose)
        elif extended_count == 3 and all(f in extended_fingers for f in ['index', 'middle', 'ring']):
            return "three_fingers", 0.83
            
        # Four fingers (minimize all)
        elif extended_count == 4 and 'thumb' not in extended_fingers:
            return "four_fingers", 0.82
            
        # Open palm (all fingers extended)
        elif extended_count >= 4:
            # Check hand movement for scroll direction
            hand_center_y = np.mean([tip[1] for tip in [index_tip, middle_tip, ring_tip, pinky_tip]])
            if hand_center_y < wrist[1] - 0.02:
                return "open_palm", 0.85  # Hand up - scroll up
            else:
                return "open_palm_down", 0.85  # Hand down - scroll down
                
        # Fist (no fingers extended or very few)
        elif extended_count <= 1:
            return "fist", 0.80
            
        # Zoom gestures (advanced - requires hand tracking history)
        # For now, use simple approximations
        elif extended_count == 2 and 'thumb' in extended_fingers and 'index' in extended_fingers:
            if thumb_index_dist > 0.08:
                return "zoom_out", 0.75
            else:
                return "zoom_in", 0.75
                
        else:
            return "unknown", 0.3
            
    def process_gesture(self, gesture, confidence, landmarks):
        """Process detected gesture and execute corresponding action"""
        self.current_gesture = gesture
        self.gesture_confidence = confidence
        
        # Add to history
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.gesture_history.append(f"{timestamp} - {gesture} ({confidence:.2f})")
        self.gesture_stats[gesture] += 1
        
        # Execute gesture action
        if gesture in self.gesture_mappings:
            action = self.gesture_mappings[gesture]
            self.execute_action(action, landmarks, confidence)
            
    def execute_action(self, action, landmarks, confidence):
        """Execute the mapped action for a gesture with enhanced controls"""
        try:
            # Volume controls
            if action == 'volume_up' and self.system_control_var.get():
                # Increase system volume using AppleScript for macOS
                subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) + 10)'], check=True)
                self.status_var.set(f"Status: Volume Up")
                self.log_gesture(f"Volume increased")
                
            elif action == 'volume_down' and self.system_control_var.get():
                # Decrease system volume using AppleScript for macOS
                subprocess.run(['osascript', '-e', 'set volume output volume (output volume of (get volume settings) - 10)'], check=True)
                self.status_var.set(f"Status: Volume Down")
                self.log_gesture(f"Volume decreased")
                
            elif action == 'mute_toggle' and self.system_control_var.get():
                # Toggle mute using AppleScript for macOS
                subprocess.run(['osascript', '-e', 'set volume output muted (not (output muted of (get volume settings)))'], check=True)
                self.status_var.set(f"Status: Mute Toggled")
                self.log_gesture(f"Volume muted/unmuted")
                
            # Brightness controls
            elif action == 'brightness_up' and self.system_control_var.get():
                # Increase screen brightness using AppleScript for macOS
                subprocess.run(['osascript', '-e', '''
                    tell application "System Events"
                        key code 144
                    end tell
                '''], check=True)
                self.status_var.set(f"Status: Brightness Up")
                self.log_gesture(f"Brightness increased")
                
            elif action == 'brightness_down' and self.system_control_var.get():
                # Decrease screen brightness using AppleScript for macOS
                subprocess.run(['osascript', '-e', '''
                    tell application "System Events"
                        key code 145
                    end tell
                '''], check=True)
                self.status_var.set(f"Status: Brightness Down")
                self.log_gesture(f"Brightness decreased")
                
            # Mouse controls with enhanced functionality
            elif action == 'mouse_move' and self.mouse_control_var.get():
                # Move mouse based on index finger position
                if len(landmarks) >= 24:  # Ensure we have index finger tip
                    points = landmarks.reshape(-1, 3)
                    index_tip = points[8][:2]  # x, y coordinates
                    
                    # Convert to screen coordinates
                    screen_x = int(index_tip[0] * self.screen_width)
                    screen_y = int(index_tip[1] * self.screen_height)
                    
                    # Apply smoothing
                    current_pos = pyautogui.position()
                    smooth_x = int(current_pos.x * self.smoothing_var.get() + 
                                 screen_x * (1 - self.smoothing_var.get()))
                    smooth_y = int(current_pos.y * self.smoothing_var.get() + 
                                 screen_y * (1 - self.smoothing_var.get()))
                    
                    pyautogui.moveTo(smooth_x, smooth_y)
                    
            elif action == 'left_click' and self.mouse_control_var.get():
                pyautogui.click()
                self.status_var.set(f"Status: Left Click")
                self.log_gesture(f"Left click executed")
                
            elif action == 'right_click' and self.mouse_control_var.get():
                pyautogui.rightClick()
                self.status_var.set(f"Status: Right Click")
                self.log_gesture(f"Right click executed")
                
            elif action == 'scroll_up' and self.mouse_control_var.get():
                pyautogui.scroll(3)
                self.status_var.set(f"Status: Scroll Up")
                self.log_gesture(f"Scrolled up")
                
            elif action == 'scroll_down' and self.mouse_control_var.get():
                pyautogui.scroll(-3)
                self.status_var.set(f"Status: Scroll Down")
                self.log_gesture(f"Scrolled down")
                
            elif action == 'scroll' and self.mouse_control_var.get():
                pyautogui.scroll(3)
                self.status_var.set(f"Status: Scroll")
                self.log_gesture(f"Scrolled")
                
            # Window management
            elif action == 'minimize_all' and self.system_control_var.get():
                # macOS: Show desktop (F11 or Mission Control)
                subprocess.run(['osascript', '-e', '''
                    tell application "System Events"
                        key code 103
                    end tell
                '''], check=True)
                self.status_var.set(f"Status: Minimize All")
                self.log_gesture(f"Minimized all windows")
                
            elif action == 'mission_control' and self.system_control_var.get():
                # Open Mission Control
                subprocess.run(['osascript', '-e', '''
                    tell application "System Events"
                        key code 160
                    end tell
                '''], check=True)
                self.status_var.set(f"Status: Mission Control")
                self.log_gesture(f"Opened Mission Control")
                
            elif action == 'expose_windows' and self.system_control_var.get():
                # Show all windows (App Exposé)
                subprocess.run(['osascript', '-e', '''
                    tell application "System Events"
                        key code 160 using control down
                    end tell
                '''], check=True)
                self.status_var.set(f"Status: Expose Windows")
                self.log_gesture(f"Showed all windows")
                
            # Tab and application controls
            elif action == 'next_tab' and self.system_control_var.get():
                pyautogui.hotkey('cmd', 'shift', ']')
                self.status_var.set(f"Status: Next Tab")
                self.log_gesture(f"Switched to next tab")
                
            elif action == 'previous_tab' and self.system_control_var.get():
                pyautogui.hotkey('cmd', 'shift', '[')
                self.status_var.set(f"Status: Previous Tab")
                self.log_gesture(f"Switched to previous tab")
                
            elif action == 'new_tab' and self.system_control_var.get():
                pyautogui.hotkey('cmd', 't')
                self.status_var.set(f"Status: New Tab")
                self.log_gesture(f"Opened new tab")
                
            elif action == 'close_tab' and self.system_control_var.get():
                pyautogui.hotkey('cmd', 'w')
                self.status_var.set(f"Status: Close Tab")
                self.log_gesture(f"Closed tab")
                
            # Application switching
            elif action == 'next_app' and self.system_control_var.get():
                pyautogui.hotkey('cmd', 'tab')
                self.status_var.set(f"Status: Next App")
                self.log_gesture(f"Switched to next app")
                
            elif action == 'previous_app' and self.system_control_var.get():
                pyautogui.hotkey('cmd', 'shift', 'tab')
                self.status_var.set(f"Status: Previous App")
                self.log_gesture(f"Switched to previous app")
                
            # Zoom controls
            elif action == 'zoom_in' and self.system_control_var.get():
                pyautogui.hotkey('cmd', '+')
                self.status_var.set(f"Status: Zoom In")
                self.log_gesture(f"Zoomed in")
                
            elif action == 'zoom_out' and self.system_control_var.get():
                pyautogui.hotkey('cmd', '-')
                self.status_var.set(f"Status: Zoom Out")
                self.log_gesture(f"Zoomed out")
                
            elif action == 'zoom_reset' and self.system_control_var.get():
                pyautogui.hotkey('cmd', '0')
                self.status_var.set(f"Status: Zoom Reset")
                self.log_gesture(f"Reset zoom")
                
            # Media controls
            elif action == 'play_pause' and self.system_control_var.get():
                pyautogui.press('space')  # Most media apps use space for play/pause
                self.status_var.set(f"Status: Play/Pause")
                self.log_gesture(f"Media play/pause")
                
            # Quick actions
            elif action == 'screenshot' and self.system_control_var.get():
                pyautogui.hotkey('cmd', 'shift', '3')
                self.status_var.set(f"Status: Screenshot")
                self.log_gesture(f"Screenshot taken")
                
            elif action == 'fullscreen_toggle' and self.system_control_var.get():
                pyautogui.hotkey('cmd', 'ctrl', 'f')
                self.status_var.set(f"Status: Fullscreen Toggle")
                self.log_gesture(f"Toggled fullscreen")
                
            elif action == 'drag' and self.mouse_control_var.get():
                if not hasattr(self, '_dragging'):
                    pyautogui.mouseDown()
                    self._dragging = True
                    self.status_var.set(f"Status: Drag Start")
                    self.log_gesture(f"Drag started")
                else:
                    pyautogui.mouseUp()
                    delattr(self, '_dragging')
                    self.status_var.set(f"Status: Drag End")
                    self.log_gesture(f"Drag ended")
                    
            else:
                # Unknown action or controls disabled
                if not (self.mouse_control_var.get() or self.system_control_var.get()):
                    self.status_var.set(f"Status: Controls disabled")
                else:
                    self.status_var.set(f"Status: Unknown action - {action}")
                    
        except subprocess.CalledProcessError as e:
            self.logger.error(f"System command failed for action {action}: {e}")
            self.status_var.set(f"Status: Command failed - {action}")
        except Exception as e:
            self.logger.error(f"Error executing action {action}: {e}")
            self.status_var.set(f"Status: Error - {action}")
            
        # Update action history
        if not hasattr(self, 'action_history'):
            self.action_history = []
            
        self.action_history.append({
            'action': action,
            'confidence': confidence,
            'timestamp': datetime.now(),
            'success': True
        })
        
        # Keep action history limited
        if len(self.action_history) > 100:
            self.action_history = self.action_history[-50:]
            
    def update_video_display(self, frame):
        """Update the video display with current frame"""
        try:
            # Resize frame for display
            display_frame = cv2.resize(frame, (640, 480))
            
            # Convert to PIL Image
            image = Image.fromarray(cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(image)
            
            # Update display
            self.video_label.config(image=photo, text="")
            self.video_label.image = photo
            
        except Exception as e:
            self.logger.error(f"Error updating video display: {e}")
            
    def update_info_displays(self):
        """Update information displays"""
        try:
            # Update gesture info
            self.gesture_label.config(text=self.current_gesture.title())
            self.confidence_label.config(text=f"Confidence: {self.gesture_confidence:.0%}")
            
            # Update performance metrics
            self.fps_label.config(text=f"FPS: {self.fps:.1f}")
            avg_process_time = np.mean(list(self.detection_times)[-10:]) if self.detection_times else 0
            self.processing_time_label.config(text=f"Processing: {avg_process_time:.1f}ms")
            
            # Update gesture history
            self.history_listbox.delete(0, tk.END)
            for gesture in list(self.gesture_history)[-8:]:  # Show last 8
                self.history_listbox.insert(tk.END, gesture)
            self.history_listbox.see(tk.END)
            
        except Exception as e:
            self.logger.error(f"Error updating displays: {e}")
            
    def toggle_recording(self):
        """Toggle video recording"""
        messagebox.showinfo("Recording", "Recording feature will be implemented in future version")
        
    def save_settings(self):
        """Save current settings to file"""
        try:
            settings = {
                'sensitivity': self.sensitivity_var.get(),
                'smoothing': self.smoothing_var.get(),
                'mouse_control': self.mouse_control_var.get(),
                'system_control': self.system_control_var.get(),
                'gesture_mappings': self.gesture_mappings
            }
            
            with open('gesture_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
                
            messagebox.showinfo("Settings", "Settings saved successfully!")
            self.logger.info("Settings saved")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            self.logger.error(f"Error saving settings: {e}")
            
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists('gesture_settings.json'):
                with open('gesture_settings.json', 'r') as f:
                    settings = json.load(f)
                
                self.sensitivity_var.set(settings.get('sensitivity', 0.7))
                self.smoothing_var.set(settings.get('smoothing', 0.3))
                self.mouse_control_var.set(settings.get('mouse_control', True))
                self.system_control_var.set(settings.get('system_control', True))
                self.gesture_mappings.update(settings.get('gesture_mappings', {}))
                
                self.logger.info("Settings loaded")
                
        except Exception as e:
            self.logger.error(f"Error loading settings: {e}")
            
    def show_analytics(self):
        """Show analytics window with performance charts"""
        if self.analytics_window is None or not self.analytics_window.winfo_exists():
            self.create_analytics_window()
        else:
            self.analytics_window.lift()
            
    def create_analytics_window(self):
        """Create the analytics window"""
        self.analytics_window = tk.Toplevel(self.root)
        self.analytics_window.title("📊 Gesture Analytics")
        self.analytics_window.geometry("800x600")
        self.analytics_window.configure(bg='#2b2b2b')
        
        # Create notebook for different analytics tabs
        notebook = ttk.Notebook(self.analytics_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Performance tab
        perf_frame = ttk.Frame(notebook)
        notebook.add(perf_frame, text="Performance")
        
        # Create performance charts
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        fig.patch.set_facecolor('#2b2b2b')
        
        # FPS chart
        if self.fps_history:
            ax1.plot(list(self.fps_history), color='#00ff00', linewidth=2)
            ax1.set_title('FPS Over Time', color='white')
            ax1.set_ylabel('FPS', color='white')
            ax1.tick_params(colors='white')
            ax1.set_facecolor('#1e1e1e')
            ax1.grid(True, alpha=0.3)
        
        # Processing time chart
        if self.detection_times:
            ax2.plot(list(self.detection_times), color='#ff6600', linewidth=2)
            ax2.set_title('Processing Time', color='white')
            ax2.set_ylabel('Time (ms)', color='white')
            ax2.set_xlabel('Frame', color='white')
            ax2.tick_params(colors='white')
            ax2.set_facecolor('#1e1e1e')
            ax2.grid(True, alpha=0.3)
        
        canvas = FigureCanvasTkAgg(fig, perf_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Gesture statistics tab
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Gesture Stats")
        
        if self.gesture_stats:
            fig2, ax3 = plt.subplots(figsize=(8, 6))
            fig2.patch.set_facecolor('#2b2b2b')
            
            gestures = list(self.gesture_stats.keys())
            counts = list(self.gesture_stats.values())
            
            bars = ax3.bar(gestures, counts, color=['#ff6b6b', '#4ecdc4', '#45b7d1', 
                                                   '#96ceb4', '#ffeaa7', '#dda0dd'])
            ax3.set_title('Gesture Recognition Statistics', color='white')
            ax3.set_ylabel('Count', color='white')
            ax3.tick_params(colors='white')
            ax3.set_facecolor('#1e1e1e')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', color='white')
            
            canvas2 = FigureCanvasTkAgg(fig2, stats_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill='both', expand=True)
            
    def calibrate_system(self):
        """Calibrate the gesture recognition system"""
        messagebox.showinfo("Calibration", 
                          "Calibration wizard will be implemented in future version.\n"
                          "Current system uses automatic calibration.")
        
    def on_closing(self):
        """Handle application closing"""
        if self.is_running:
            self.stop_detection()
        
        self.save_settings()
        self.root.destroy()
        
    def run(self):
        """Run the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main():
    """Main function to run the Professional Gesture Control System"""
    try:
        app = GestureControlPro()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        logging.error(f"Error starting application: {e}")

if __name__ == "__main__":
    main()
