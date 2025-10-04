#!/usr/bin/env python3
"""
Professional Simple Hand Tracking System
========================================
A fallback professional GUI application for systems where MediaPipe 
might not be available. Uses color-based hand detection with advanced
GUI features and real-time analytics.
"""

import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pyautogui
import threading
import time
import json
import os
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque, defaultdict
import logging
from datetime import datetime

# Disable PyAutoGUI failsafe
pyautogui.FAILSAFE = False

class SimpleTrackingPro:
    def __init__(self):
        """Initialize the Professional Simple Tracking System"""
        self.setup_logging()
        self.setup_variables()
        self.setup_gui()
        self.load_settings()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('simple_tracking.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_variables(self):
        """Initialize application variables"""
        # Camera and detection variables
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.fps = 0
        self.frame_count = 0
        
        # Color detection parameters
        self.h_low = 0
        self.h_high = 25
        self.s_low = 50
        self.s_high = 255
        self.v_low = 50
        self.v_high = 255
        
        # Tracking variables
        self.current_position = (0, 0)
        self.previous_positions = deque(maxlen=10)
        self.gesture_state = "None"
        self.click_cooldown = 1.0
        self.last_click_time = 0
        
        # Performance metrics
        self.fps_history = deque(maxlen=100)
        self.detection_times = deque(maxlen=100)
        self.tracking_stats = defaultdict(int)
        
        # Screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Control variables
        self.sensitivity = 3000  # Minimum area for hand detection
        self.smoothing = 0.3
        self.mouse_control_enabled = True
        
    def setup_gui(self):
        """Create the professional GUI interface"""
        self.root = tk.Tk()
        self.root.title("Professional Simple Hand Tracking System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Create main layout
        self.create_header()
        self.create_main_content()
        self.create_control_panel()
        self.create_status_bar()
        
    def create_header(self):
        """Create the application header"""
        header_frame = tk.Frame(self.root, bg='#1e1e1e', height=60)
        header_frame.pack(fill='x', padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🎯 Professional Simple Hand Tracking",
                              font=('Arial', 18, 'bold'),
                              fg='#00ff00', bg='#1e1e1e')
        title_label.pack(side='left', padx=20, pady=15)
        
        # Status indicators
        self.status_frame = tk.Frame(header_frame, bg='#1e1e1e')
        self.status_frame.pack(side='right', padx=20, pady=15)
        
        self.camera_status = tk.Label(self.status_frame, text="📷 Camera: OFF",
                                     fg='red', bg='#1e1e1e', font=('Arial', 10))
        self.camera_status.pack(side='right', padx=10)
        
        self.tracking_status = tk.Label(self.status_frame, text="🎯 Tracking: OFF",
                                       fg='red', bg='#1e1e1e', font=('Arial', 10))
        self.tracking_status.pack(side='right', padx=10)
        
    def create_main_content(self):
        """Create the main content area"""
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Video feeds
        video_container = tk.Frame(main_frame, bg='#2b2b2b')
        video_container.pack(side='left', fill='both', expand=True, padx=5)
        
        # Original video feed
        self.video_frame = tk.LabelFrame(video_container, text="📹 Original Feed",
                                        bg='#2b2b2b', fg='white',
                                        font=('Arial', 12, 'bold'))
        self.video_frame.pack(side='top', fill='both', expand=True, pady=2)
        
        self.video_label = tk.Label(self.video_frame, bg='black', text="Camera Feed",
                                   fg='white', font=('Arial', 14))
        self.video_label.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Mask video feed
        self.mask_frame = tk.LabelFrame(video_container, text="🎭 Detection Mask",
                                       bg='#2b2b2b', fg='white',
                                       font=('Arial', 12, 'bold'))
        self.mask_frame.pack(side='bottom', fill='both', expand=True, pady=2)
        
        self.mask_label = tk.Label(self.mask_frame, bg='black', text="Detection Mask",
                                  fg='white', font=('Arial', 14))
        self.mask_label.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Video controls
        video_controls = tk.Frame(video_container, bg='#2b2b2b')
        video_controls.pack(fill='x', padx=10, pady=5)
        
        self.start_button = tk.Button(video_controls, text="🎥 Start Tracking",
                                     command=self.start_tracking,
                                     bg='#00aa00', fg='white',
                                     font=('Arial', 10, 'bold'))
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = tk.Button(video_controls, text="⏹️ Stop Tracking",
                                    command=self.stop_tracking,
                                    bg='#aa0000', fg='white',
                                    font=('Arial', 10, 'bold'))
        self.stop_button.pack(side='left', padx=5)
        
        self.calibrate_button = tk.Button(video_controls, text="🎯 Auto Calibrate",
                                         command=self.auto_calibrate,
                                         bg='#0066cc', fg='white',
                                         font=('Arial', 10, 'bold'))
        self.calibrate_button.pack(side='left', padx=5)
        
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
        # Current tracking display
        tracking_frame = tk.LabelFrame(self.info_frame, text="Current Tracking",
                                      bg='#2b2b2b', fg='white')
        tracking_frame.pack(fill='x', padx=10, pady=5)
        
        self.position_label = tk.Label(tracking_frame, text="Position: (0, 0)",
                                      bg='#2b2b2b', fg='#00ff00',
                                      font=('Arial', 14, 'bold'))
        self.position_label.pack(pady=10)
        
        self.gesture_label = tk.Label(tracking_frame, text="Gesture: None",
                                     bg='#2b2b2b', fg='white',
                                     font=('Arial', 12))
        self.gesture_label.pack(pady=5)
        
        # Performance metrics
        perf_frame = tk.LabelFrame(self.info_frame, text="Performance",
                                  bg='#2b2b2b', fg='white')
        perf_frame.pack(fill='x', padx=10, pady=5)
        
        self.fps_label = tk.Label(perf_frame, text="FPS: 0",
                                 bg='#2b2b2b', fg='white')
        self.fps_label.pack(anchor='w', padx=10, pady=2)
        
        self.area_label = tk.Label(perf_frame, text="Detection Area: 0",
                                  bg='#2b2b2b', fg='white')
        self.area_label.pack(anchor='w', padx=10, pady=2)
        
        self.processing_time_label = tk.Label(perf_frame, text="Processing: 0ms",
                                            bg='#2b2b2b', fg='white')
        self.processing_time_label.pack(anchor='w', padx=10, pady=2)
        
        # Color calibration controls
        calib_frame = tk.LabelFrame(self.info_frame, text="Color Calibration",
                                   bg='#2b2b2b', fg='white')
        calib_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # HSV sliders
        self.create_hsv_sliders(calib_frame)
        
    def create_hsv_sliders(self, parent):
        """Create HSV adjustment sliders"""
        # Hue
        tk.Label(parent, text="Hue Range:", bg='#2b2b2b', fg='white').pack(anchor='w', padx=5)
        
        hue_frame = tk.Frame(parent, bg='#2b2b2b')
        hue_frame.pack(fill='x', padx=5, pady=2)
        
        self.h_low_var = tk.IntVar(value=self.h_low)
        tk.Scale(hue_frame, from_=0, to=179, orient='horizontal',
                variable=self.h_low_var, bg='#2b2b2b', fg='white',
                highlightbackground='#2b2b2b', length=150).pack(side='left')
        
        self.h_high_var = tk.IntVar(value=self.h_high)
        tk.Scale(hue_frame, from_=0, to=179, orient='horizontal',
                variable=self.h_high_var, bg='#2b2b2b', fg='white',
                highlightbackground='#2b2b2b', length=150).pack(side='right')
        
        # Saturation
        tk.Label(parent, text="Saturation Range:", bg='#2b2b2b', fg='white').pack(anchor='w', padx=5, pady=(5,0))
        
        sat_frame = tk.Frame(parent, bg='#2b2b2b')
        sat_frame.pack(fill='x', padx=5, pady=2)
        
        self.s_low_var = tk.IntVar(value=self.s_low)
        tk.Scale(sat_frame, from_=0, to=255, orient='horizontal',
                variable=self.s_low_var, bg='#2b2b2b', fg='white',
                highlightbackground='#2b2b2b', length=150).pack(side='left')
        
        self.s_high_var = tk.IntVar(value=self.s_high)
        tk.Scale(sat_frame, from_=0, to=255, orient='horizontal',
                variable=self.s_high_var, bg='#2b2b2b', fg='white',
                highlightbackground='#2b2b2b', length=150).pack(side='right')
        
        # Value
        tk.Label(parent, text="Value Range:", bg='#2b2b2b', fg='white').pack(anchor='w', padx=5, pady=(5,0))
        
        val_frame = tk.Frame(parent, bg='#2b2b2b')
        val_frame.pack(fill='x', padx=5, pady=2)
        
        self.v_low_var = tk.IntVar(value=self.v_low)
        tk.Scale(val_frame, from_=0, to=255, orient='horizontal',
                variable=self.v_low_var, bg='#2b2b2b', fg='white',
                highlightbackground='#2b2b2b', length=150).pack(side='left')
        
        self.v_high_var = tk.IntVar(value=self.v_high)
        tk.Scale(val_frame, from_=0, to=255, orient='horizontal',
                variable=self.v_high_var, bg='#2b2b2b', fg='white',
                highlightbackground='#2b2b2b', length=150).pack(side='right')
        
    def create_control_panel(self):
        """Create the control panel"""
        control_frame = tk.LabelFrame(self.root, text="🎛️ Control Panel",
                                     bg='#2b2b2b', fg='white',
                                     font=('Arial', 12, 'bold'))
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Settings section
        settings_frame = tk.Frame(control_frame, bg='#2b2b2b')
        settings_frame.pack(side='left', fill='y', padx=10, pady=10)
        
        tk.Label(settings_frame, text="Sensitivity (Min Area):",
                bg='#2b2b2b', fg='white').pack(anchor='w')
        
        self.sensitivity_var = tk.IntVar(value=3000)
        self.sensitivity_scale = tk.Scale(settings_frame, from_=500, to=10000,
                                         resolution=100, orient='horizontal',
                                         variable=self.sensitivity_var,
                                         bg='#2b2b2b', fg='white',
                                         highlightbackground='#2b2b2b')
        self.sensitivity_scale.pack(fill='x')
        
        tk.Label(settings_frame, text="Mouse Smoothing:",
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
        
        tk.Button(buttons_frame, text="🔄 Reset Calibration",
                 command=self.reset_calibration,
                 bg='#cc6600', fg='white',
                 font=('Arial', 9, 'bold')).pack(pady=2, fill='x')
        
    def create_status_bar(self):
        """Create the status bar"""
        status_frame = tk.Frame(self.root, bg='#1e1e1e', height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_text = tk.Label(status_frame, text="Ready - Simple Color-Based Tracking",
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
        """Update time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def start_tracking(self):
        """Start the hand tracking system"""
        if not self.is_running:
            try:
                self.cap = cv2.VideoCapture(0)
                if not self.cap.isOpened():
                    messagebox.showerror("Error", "Could not access camera")
                    return
                
                self.is_running = True
                self.camera_status.config(text="📷 Camera: ON", fg='green')
                self.tracking_status.config(text="🎯 Tracking: ON", fg='green')
                self.status_text.config(text="Tracking Active - Move your hand in front of camera")
                
                # Start tracking thread
                self.tracking_thread = threading.Thread(target=self.tracking_loop)
                self.tracking_thread.daemon = True
                self.tracking_thread.start()
                
                self.logger.info("Hand tracking started")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start tracking: {str(e)}")
                self.logger.error(f"Error starting tracking: {e}")
                
    def stop_tracking(self):
        """Stop the tracking system"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        
        self.camera_status.config(text="📷 Camera: OFF", fg='red')
        self.tracking_status.config(text="🎯 Tracking: OFF", fg='red')
        self.status_text.config(text="Tracking Stopped")
        
        # Clear displays
        self.video_label.config(image='', text="Camera Feed")
        self.mask_label.config(image='', text="Detection Mask")
        
        self.logger.info("Hand tracking stopped")
        
    def tracking_loop(self):
        """Main tracking loop"""
        prev_time = time.time()
        
        while self.is_running:
            try:
                start_process = time.time()
                
                ret, frame = self.cap.read()
                if not ret:
                    continue
                
                # Flip frame for mirror effect
                frame = cv2.flip(frame, 1)
                frame_height, frame_width = frame.shape[:2]
                
                # Convert to HSV
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                
                # Get current HSV values
                self.update_hsv_values()
                
                # Create mask
                lower = np.array([self.h_low, self.s_low, self.v_low])
                upper = np.array([self.h_high, self.s_high, self.v_high])
                mask = cv2.inRange(hsv, lower, upper)
                
                # Apply morphological operations
                kernel = np.ones((5, 5), np.uint8)
                mask = cv2.erode(mask, kernel, iterations=1)
                mask = cv2.dilate(mask, kernel, iterations=2)
                
                # Find contours
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                detection_area = 0
                if contours:
                    # Find largest contour
                    largest_contour = max(contours, key=cv2.contourArea)
                    detection_area = cv2.contourArea(largest_contour)
                    
                    # Only process if area is large enough
                    if detection_area > self.sensitivity_var.get():
                        self.process_hand_detection(largest_contour, frame, frame_width, frame_height)
                    else:
                        self.gesture_state = "None"
                
                # Calculate FPS
                current_time = time.time()
                fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
                prev_time = current_time
                self.fps = fps
                self.fps_history.append(fps)
                
                # Record processing time
                process_time = (time.time() - start_process) * 1000
                self.detection_times.append(process_time)
                
                # Update displays
                self.update_video_displays(frame, mask)
                self.update_info_displays(detection_area)
                
                time.sleep(0.01)
                
            except Exception as e:
                self.logger.error(f"Error in tracking loop: {e}")
                time.sleep(0.1)
                
    def update_hsv_values(self):
        """Update HSV values from sliders"""
        self.h_low = self.h_low_var.get()
        self.h_high = self.h_high_var.get()
        self.s_low = self.s_low_var.get()
        self.s_high = self.s_high_var.get()
        self.v_low = self.v_low_var.get()
        self.v_high = self.v_high_var.get()
        
    def process_hand_detection(self, contour, frame, frame_width, frame_height):
        """Process detected hand contour"""
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Calculate centroid
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Draw centroid
            cv2.circle(frame, (cx, cy), 7, (0, 0, 255), -1)
            
            # Update position
            self.current_position = (cx, cy)
            self.previous_positions.append((cx, cy))
            
            # Control mouse if enabled
            if self.mouse_control_var.get():
                self.control_mouse(cx, cy, frame_width, frame_height)
            
            # Detect gesture based on contour properties
            self.detect_simple_gesture(w, h, contour)
            
    def control_mouse(self, x, y, frame_width, frame_height):
        """Control mouse cursor based on hand position"""
        try:
            # Map to screen coordinates
            screen_x = int((x / frame_width) * self.screen_width)
            screen_y = int((y / frame_height) * self.screen_height)
            
            # Apply smoothing
            current_pos = pyautogui.position()
            smoothing = self.smoothing_var.get()
            smooth_x = int(current_pos.x * smoothing + screen_x * (1 - smoothing))
            smooth_y = int(current_pos.y * smoothing + screen_y * (1 - smoothing))
            
            # Move mouse
            pyautogui.moveTo(smooth_x, smooth_y)
            
        except Exception as e:
            self.logger.error(f"Error controlling mouse: {e}")
            
    def detect_simple_gesture(self, width, height, contour):
        """Simple gesture detection based on contour properties"""
        aspect_ratio = float(height) / width if width > 0 else 0
        
        # Simple gesture classification
        if 0.8 < aspect_ratio < 1.2:
            self.gesture_state = "Fist (Click)"
            
            # Perform click with cooldown
            current_time = time.time()
            if current_time - self.last_click_time > self.click_cooldown:
                if self.mouse_control_var.get():
                    pyautogui.click()
                self.last_click_time = current_time
                self.tracking_stats["clicks"] += 1
                
        elif aspect_ratio < 0.6:
            self.gesture_state = "Open Hand (Wide)"
        elif aspect_ratio > 1.5:
            self.gesture_state = "Pointing (Tall)"
        else:
            self.gesture_state = "Hand Detected"
            
    def update_video_displays(self, frame, mask):
        """Update video displays"""
        try:
            # Original frame
            display_frame = cv2.resize(frame, (320, 240))
            image = Image.fromarray(cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(image)
            self.video_label.config(image=photo, text="")
            self.video_label.image = photo
            
            # Mask frame
            mask_colored = cv2.applyColorMap(mask, cv2.COLORMAP_JET)
            display_mask = cv2.resize(mask_colored, (320, 240))
            mask_image = Image.fromarray(cv2.cvtColor(display_mask, cv2.COLOR_BGR2RGB))
            mask_photo = ImageTk.PhotoImage(mask_image)
            self.mask_label.config(image=mask_photo, text="")
            self.mask_label.image = mask_photo
            
        except Exception as e:
            self.logger.error(f"Error updating video displays: {e}")
            
    def update_info_displays(self, detection_area):
        """Update information displays"""
        try:
            # Position info
            self.position_label.config(text=f"Position: {self.current_position}")
            self.gesture_label.config(text=f"Gesture: {self.gesture_state}")
            
            # Performance metrics
            self.fps_label.config(text=f"FPS: {self.fps:.1f}")
            self.area_label.config(text=f"Detection Area: {int(detection_area)}")
            
            avg_process_time = np.mean(list(self.detection_times)[-10:]) if self.detection_times else 0
            self.processing_time_label.config(text=f"Processing: {avg_process_time:.1f}ms")
            
        except Exception as e:
            self.logger.error(f"Error updating info displays: {e}")
            
    def auto_calibrate(self):
        """Auto-calibrate skin color detection"""
        messagebox.showinfo("Auto Calibration", 
                          "Place your hand in the center of the camera view and click OK.\n"
                          "Make sure your hand is well-lit and clearly visible.")
        
        if not self.is_running:
            messagebox.showwarning("Warning", "Please start tracking first")
            return
            
        # Simple auto-calibration - adjust to common skin tone ranges
        self.h_low_var.set(0)
        self.h_high_var.set(30)
        self.s_low_var.set(30)
        self.s_high_var.set(255)
        self.v_low_var.set(60)
        self.v_high_var.set(255)
        
        messagebox.showinfo("Calibration", "Auto-calibration completed!")
        
    def reset_calibration(self):
        """Reset calibration to default values"""
        self.h_low_var.set(0)
        self.h_high_var.set(25)
        self.s_low_var.set(50)
        self.s_high_var.set(255)
        self.v_low_var.set(50)
        self.v_high_var.set(255)
        
        messagebox.showinfo("Reset", "Calibration reset to default values")
        
    def save_settings(self):
        """Save current settings"""
        try:
            settings = {
                'h_low': self.h_low_var.get(),
                'h_high': self.h_high_var.get(),
                's_low': self.s_low_var.get(),
                's_high': self.s_high_var.get(),
                'v_low': self.v_low_var.get(),
                'v_high': self.v_high_var.get(),
                'sensitivity': self.sensitivity_var.get(),
                'smoothing': self.smoothing_var.get(),
                'mouse_control': self.mouse_control_var.get()
            }
            
            with open('simple_tracking_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
                
            messagebox.showinfo("Settings", "Settings saved successfully!")
            self.logger.info("Settings saved")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists('simple_tracking_settings.json'):
                with open('simple_tracking_settings.json', 'r') as f:
                    settings = json.load(f)
                
                self.h_low = settings.get('h_low', 0)
                self.h_high = settings.get('h_high', 25)
                self.s_low = settings.get('s_low', 50)
                self.s_high = settings.get('s_high', 255)
                self.v_low = settings.get('v_low', 50)
                self.v_high = settings.get('v_high', 255)
                
                self.logger.info("Settings loaded")
                
        except Exception as e:
            self.logger.error(f"Error loading settings: {e}")
            
    def show_analytics(self):
        """Show analytics window"""
        analytics_window = tk.Toplevel(self.root)
        analytics_window.title("📊 Tracking Analytics")
        analytics_window.geometry("600x500")
        analytics_window.configure(bg='#2b2b2b')
        
        # Performance chart
        if self.fps_history:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5))
            fig.patch.set_facecolor('#2b2b2b')
            
            # FPS chart
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
            
            canvas = FigureCanvasTkAgg(fig, analytics_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
            
    def on_closing(self):
        """Handle application closing"""
        if self.is_running:
            self.stop_tracking()
        
        self.save_settings()
        self.root.destroy()
        
    def run(self):
        """Run the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = SimpleTrackingPro()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        logging.error(f"Error starting application: {e}")

if __name__ == "__main__":
    main()
