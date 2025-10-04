#!/usr/bin/env python3
"""
Advanced Feature Test Suite
===========================
Test all the advanced gesture control features to ensure they work properly.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import time

class FeatureTestSuite:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 Advanced Features Test Suite")
        self.root.geometry("700x800")
        self.root.configure(bg='#1a1a1a')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', 
                           background='#1a1a1a', 
                           foreground='#00ff41', 
                           font=('Monaco', 16, 'bold'))
        self.style.configure('Test.TButton', 
                           background='#2d2d2d', 
                           foreground='#ffffff',
                           font=('Monaco', 10))
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = ttk.Label(self.root, text="🎛️ Advanced Gesture Control Test Suite", 
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Create scrollable frame
        canvas = tk.Canvas(self.root, bg='#1a1a1a', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#1a1a1a')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Test sections
        self.create_volume_tests()
        self.create_brightness_tests()
        self.create_window_tests()
        self.create_navigation_tests()
        self.create_media_tests()
        self.create_system_tests()
        
        # Results area
        self.create_results_area()
        
    def create_section(self, title, description):
        """Create a test section with title and description"""
        section_frame = tk.Frame(self.scrollable_frame, bg='#2d2d2d', relief='raised', bd=2)
        section_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(section_frame, text=title, 
                              bg='#2d2d2d', fg='#00ff41', 
                              font=('Monaco', 12, 'bold'))
        title_label.pack(anchor='w', padx=10, pady=5)
        
        desc_label = tk.Label(section_frame, text=description, 
                             bg='#2d2d2d', fg='#ffffff', 
                             font=('Monaco', 9), wraplength=600)
        desc_label.pack(anchor='w', padx=10, pady=(0, 5))
        
        return section_frame
        
    def create_volume_tests(self):
        section = self.create_section("🔊 Volume Controls", 
                                    "Test volume up, down, and mute functionality")
        
        button_frame = tk.Frame(section, bg='#2d2d2d')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="🔊 Test Volume Up", 
                  command=lambda: self.test_volume_up(),
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔉 Test Volume Down", 
                  command=lambda: self.test_volume_down(),
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔇 Test Mute Toggle", 
                  command=lambda: self.test_mute(),
                  style='Test.TButton').pack(side='left', padx=5)
                  
    def create_brightness_tests(self):
        section = self.create_section("💡 Brightness Controls", 
                                    "Test screen brightness adjustment")
        
        button_frame = tk.Frame(section, bg='#2d2d2d')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="☀️ Brightness Up", 
                  command=lambda: self.test_brightness_up(),
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="🌙 Brightness Down", 
                  command=lambda: self.test_brightness_down(),
                  style='Test.TButton').pack(side='left', padx=5)
                  
    def create_window_tests(self):
        section = self.create_section("🪟 Window Management", 
                                    "Test window and desktop management")
        
        button_frame = tk.Frame(section, bg='#2d2d2d')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="🏠 Show Desktop", 
                  command=lambda: self.test_show_desktop(),
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="🎛️ Mission Control", 
                  command=lambda: self.test_mission_control(),
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="📱 App Exposé", 
                  command=lambda: self.test_expose(),
                  style='Test.TButton').pack(side='left', padx=5)
                  
    def create_navigation_tests(self):
        section = self.create_section("🗂️ Navigation Controls", 
                                    "Test tab switching and app navigation")
        
        button_frame = tk.Frame(section, bg='#2d2d2d')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="➡️ Next Tab", 
                  command=lambda: self.test_next_tab(),
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="⬅️ Previous Tab", 
                  command=lambda: self.test_prev_tab(),
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔄 App Switch", 
                  command=lambda: self.test_app_switch(),
                  style='Test.TButton').pack(side='left', padx=5)
                  
    def create_media_tests(self):
        section = self.create_section("🎵 Media Controls", 
                                    "Test media playback controls")
        
        button_frame = tk.Frame(section, bg='#2d2d2d')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="⏯️ Play/Pause", 
                  command=lambda: self.test_play_pause(),
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="⏭️ Next Track", 
                  command=lambda: self.test_next_track(),
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="⏮️ Previous Track", 
                  command=lambda: self.test_prev_track(),
                  style='Test.TButton').pack(side='left', padx=5)
                  
    def create_system_tests(self):
        section = self.create_section("⚡ Quick Actions", 
                                    "Test system shortcuts and quick actions")
        
        button_frame = tk.Frame(section, bg='#2d2d2d')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="📸 Screenshot", 
                  command=lambda: self.test_screenshot(),
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔍 Zoom In", 
                  command=lambda: self.test_zoom_in(),
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔍 Zoom Out", 
                  command=lambda: self.test_zoom_out(),
                  style='Test.TButton').pack(side='left', padx=5)
                  
    def create_results_area(self):
        # Results section
        results_frame = tk.Frame(self.scrollable_frame, bg='#2d2d2d', relief='raised', bd=2)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        results_title = tk.Label(results_frame, text="🧪 Test Results", 
                                bg='#2d2d2d', fg='#00ff41', 
                                font=('Monaco', 12, 'bold'))
        results_title.pack(anchor='w', padx=10, pady=5)
        
        # Results text area
        self.results_text = tk.Text(results_frame, 
                                   bg='#1a1a1a', fg='#ffffff',
                                   font=('Monaco', 9),
                                   height=8, wrap='word')
        self.results_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Control buttons
        control_frame = tk.Frame(results_frame, bg='#2d2d2d')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="🧹 Clear Results", 
                  command=self.clear_results,
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="🚀 Launch Main App", 
                  command=self.launch_main_app,
                  style='Test.TButton').pack(side='left', padx=5)
        ttk.Button(control_frame, text="📋 Copy Results", 
                  command=self.copy_results,
                  style='Test.TButton').pack(side='left', padx=5)
                  
        # Initial message
        self.log_result("🎯 Advanced Feature Test Suite Ready!")
        self.log_result("Click any test button to verify functionality.")
        self.log_result("Tests will execute system commands - you should see/hear the results.")
        self.log_result("-" * 50)
        
    def log_result(self, message):
        """Log test result to the results area"""
        self.results_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.results_text.see(tk.END)
        self.results_text.update()
        
    def run_command(self, cmd, test_name):
        """Run a system command and log the result"""
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            self.log_result(f"✅ {test_name} - Command executed successfully")
        except subprocess.CalledProcessError as e:
            self.log_result(f"❌ {test_name} - Command failed: {e}")
        except Exception as e:
            self.log_result(f"❌ {test_name} - Error: {e}")
            
    # Test methods
    def test_volume_up(self):
        self.log_result("🔊 Testing Volume Up...")
        cmd = ['osascript', '-e', 'set volume output volume (output volume of (get volume settings) + 10)']
        self.run_command(cmd, "Volume Up")
        
    def test_volume_down(self):
        self.log_result("🔉 Testing Volume Down...")
        cmd = ['osascript', '-e', 'set volume output volume (output volume of (get volume settings) - 10)']
        self.run_command(cmd, "Volume Down")
        
    def test_mute(self):
        self.log_result("🔇 Testing Mute Toggle...")
        cmd = ['osascript', '-e', 'set volume output muted (not (output muted of (get volume settings)))']
        self.run_command(cmd, "Mute Toggle")
        
    def test_brightness_up(self):
        self.log_result("☀️ Testing Brightness Up...")
        cmd = ['osascript', '-e', '''
            tell application "System Events"
                key code 144
            end tell
        ''']
        self.run_command(cmd, "Brightness Up")
        
    def test_brightness_down(self):
        self.log_result("🌙 Testing Brightness Down...")
        cmd = ['osascript', '-e', '''
            tell application "System Events"
                key code 145
            end tell
        ''']
        self.run_command(cmd, "Brightness Down")
        
    def test_show_desktop(self):
        self.log_result("🏠 Testing Show Desktop...")
        cmd = ['osascript', '-e', '''
            tell application "System Events"
                key code 103
            end tell
        ''']
        self.run_command(cmd, "Show Desktop")
        
    def test_mission_control(self):
        self.log_result("🎛️ Testing Mission Control...")
        cmd = ['osascript', '-e', '''
            tell application "System Events"
                key code 160
            end tell
        ''']
        self.run_command(cmd, "Mission Control")
        
    def test_expose(self):
        self.log_result("📱 Testing App Exposé...")
        cmd = ['osascript', '-e', '''
            tell application "System Events"
                key code 160 using control down
            end tell
        ''']
        self.run_command(cmd, "App Exposé")
        
    def test_next_tab(self):
        self.log_result("➡️ Testing Next Tab...")
        try:
            import pyautogui
            pyautogui.hotkey('cmd', 'shift', ']')
            self.log_result("✅ Next Tab - Hotkey executed successfully")
        except Exception as e:
            self.log_result(f"❌ Next Tab - Error: {e}")
            
    def test_prev_tab(self):
        self.log_result("⬅️ Testing Previous Tab...")
        try:
            import pyautogui
            pyautogui.hotkey('cmd', 'shift', '[')
            self.log_result("✅ Previous Tab - Hotkey executed successfully")
        except Exception as e:
            self.log_result(f"❌ Previous Tab - Error: {e}")
            
    def test_app_switch(self):
        self.log_result("🔄 Testing App Switch...")
        try:
            import pyautogui
            pyautogui.hotkey('cmd', 'tab')
            self.log_result("✅ App Switch - Hotkey executed successfully")
        except Exception as e:
            self.log_result(f"❌ App Switch - Error: {e}")
            
    def test_play_pause(self):
        self.log_result("⏯️ Testing Play/Pause...")
        try:
            import pyautogui
            pyautogui.press('space')
            self.log_result("✅ Play/Pause - Space key sent successfully")
        except Exception as e:
            self.log_result(f"❌ Play/Pause - Error: {e}")
            
    def test_next_track(self):
        self.log_result("⏭️ Testing Next Track...")
        cmd = ['osascript', '-e', '''
            tell application "System Events"
                key code 124 using function down
            end tell
        ''']
        self.run_command(cmd, "Next Track")
        
    def test_prev_track(self):
        self.log_result("⏮️ Testing Previous Track...")
        cmd = ['osascript', '-e', '''
            tell application "System Events"
                key code 123 using function down
            end tell
        ''']
        self.run_command(cmd, "Previous Track")
        
    def test_screenshot(self):
        self.log_result("📸 Testing Screenshot...")
        try:
            import pyautogui
            pyautogui.hotkey('cmd', 'shift', '3')
            self.log_result("✅ Screenshot - Shortcut executed successfully")
        except Exception as e:
            self.log_result(f"❌ Screenshot - Error: {e}")
            
    def test_zoom_in(self):
        self.log_result("🔍 Testing Zoom In...")
        try:
            import pyautogui
            pyautogui.hotkey('cmd', '+')
            self.log_result("✅ Zoom In - Hotkey executed successfully")
        except Exception as e:
            self.log_result(f"❌ Zoom In - Error: {e}")
            
    def test_zoom_out(self):
        self.log_result("🔍 Testing Zoom Out...")
        try:
            import pyautogui
            pyautogui.hotkey('cmd', '-')
            self.log_result("✅ Zoom Out - Hotkey executed successfully")
        except Exception as e:
            self.log_result(f"❌ Zoom Out - Error: {e}")
            
    def clear_results(self):
        """Clear the results text area"""
        self.results_text.delete(1.0, tk.END)
        self.log_result("🧹 Results cleared.")
        
    def copy_results(self):
        """Copy results to clipboard"""
        try:
            results = self.results_text.get(1.0, tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(results)
            self.log_result("📋 Results copied to clipboard!")
        except Exception as e:
            self.log_result(f"❌ Copy failed: {e}")
            
    def launch_main_app(self):
        """Launch the main gesture control application"""
        try:
            import os
            import threading
            
            def launch():
                os.system("python3 gesture_control_pro.py")
                
            thread = threading.Thread(target=launch, daemon=True)
            thread.start()
            self.log_result("🚀 Main application launched in background!")
            
        except Exception as e:
            self.log_result(f"❌ Launch failed: {e}")
            
    def run(self):
        """Start the test suite application"""
        self.root.mainloop()

if __name__ == "__main__":
    print("🚀 Starting Advanced Features Test Suite...")
    app = FeatureTestSuite()
    app.run()
