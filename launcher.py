#!/usr/bin/env python3
"""
Professional Gesture Control Launcher
====================================
Intelligent launcher that detects available libraries and launches
the most appropriate version of the gesture control system.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import logging

class GestureLauncher:
    def __init__(self):
        self.setup_gui()
        self.check_dependencies()
        
    def setup_gui(self):
        """Create launcher GUI"""
        self.root = tk.Tk()
        self.root.title("🚀 Professional Gesture Control Launcher")
        self.root.geometry("600x500")
        self.root.configure(bg='#2b2b2b')
        self.root.resizable(False, False)
        
        # Header
        header_frame = tk.Frame(self.root, bg='#1e1e1e', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="🤖 Professional AI Gesture Control",
                              font=('Arial', 20, 'bold'),
                              fg='#00ff00', bg='#1e1e1e')
        title_label.pack(pady=20)
        
        # Main content
        main_frame = tk.LabelFrame(self.root, text="📋 System Check & Launch Options",
                                  bg='#2b2b2b', fg='white',
                                  font=('Arial', 14, 'bold'))
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # System status
        self.status_frame = tk.Frame(main_frame, bg='#2b2b2b')
        self.status_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(self.status_frame, text="System Dependencies:",
                font=('Arial', 12, 'bold'), bg='#2b2b2b', fg='white').pack(anchor='w')
        
        # Create status labels
        self.python_status = tk.Label(self.status_frame, text="🐍 Python: Checking...",
                                     bg='#2b2b2b', fg='yellow', font=('Arial', 10))
        self.python_status.pack(anchor='w', pady=2)
        
        self.opencv_status = tk.Label(self.status_frame, text="📷 OpenCV: Checking...",
                                     bg='#2b2b2b', fg='yellow', font=('Arial', 10))
        self.opencv_status.pack(anchor='w', pady=2)
        
        self.mediapipe_status = tk.Label(self.status_frame, text="🧠 MediaPipe: Checking...",
                                        bg='#2b2b2b', fg='yellow', font=('Arial', 10))
        self.mediapipe_status.pack(anchor='w', pady=2)
        
        self.pyautogui_status = tk.Label(self.status_frame, text="🖱️ PyAutoGUI: Checking...",
                                        bg='#2b2b2b', fg='yellow', font=('Arial', 10))
        self.pyautogui_status.pack(anchor='w', pady=2)
        
        self.gui_status = tk.Label(self.status_frame, text="🖼️ GUI Libraries: Checking...",
                                  bg='#2b2b2b', fg='yellow', font=('Arial', 10))
        self.gui_status.pack(anchor='w', pady=2)
        
        # Recommendations
        self.recommendation_frame = tk.LabelFrame(main_frame, text="📋 Recommendations",
                                                 bg='#2b2b2b', fg='white')
        self.recommendation_frame.pack(fill='x', padx=20, pady=10)
        
        self.recommendation_text = tk.Text(self.recommendation_frame, height=6, width=60,
                                          bg='#1e1e1e', fg='white', wrap=tk.WORD,
                                          font=('Arial', 10))
        self.recommendation_text.pack(padx=10, pady=10)
        
        # Launch buttons
        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        self.advanced_button = tk.Button(button_frame, 
                                        text="🎯 Launch Advanced Version (MediaPipe)",
                                        command=self.launch_advanced,
                                        bg='#00aa00', fg='white',
                                        font=('Arial', 12, 'bold'),
                                        height=2, state='disabled')
        self.advanced_button.pack(fill='x', pady=5)
        
        self.simple_button = tk.Button(button_frame,
                                      text="🎨 Launch Simple Version (Color Tracking)",
                                      command=self.launch_simple,
                                      bg='#0066cc', fg='white',
                                      font=('Arial', 12, 'bold'),
                                      height=2, state='disabled')
        self.simple_button.pack(fill='x', pady=5)
        
        self.install_button = tk.Button(button_frame,
                                       text="⬇️ Install Missing Dependencies",
                                       command=self.install_dependencies,
                                       bg='#cc6600', fg='white',
                                       font=('Arial', 12, 'bold'),
                                       height=2)
        self.install_button.pack(fill='x', pady=5)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg='#1e1e1e', height=40)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        tk.Label(footer_frame, text="Professional Gesture Control System v2.0",
                bg='#1e1e1e', fg='#888888', font=('Arial', 9)).pack(pady=10)
        
    def check_dependencies(self):
        """Check all required dependencies"""
        self.root.update()
        self.root.after(100, self._check_python)
        
    def _check_python(self):
        """Check Python version"""
        try:
            version = sys.version_info
            if version.major >= 3 and version.minor >= 7:
                self.python_status.config(text=f"🐍 Python: {version.major}.{version.minor}.{version.micro} ✅",
                                         fg='green')
                self.python_ok = True
            else:
                self.python_status.config(text=f"🐍 Python: {version.major}.{version.minor}.{version.micro} ❌ (Need 3.7+)",
                                         fg='red')
                self.python_ok = False
        except Exception as e:
            self.python_status.config(text="🐍 Python: Error checking ❌", fg='red')
            self.python_ok = False
            
        self.root.after(100, self._check_opencv)
        
    def _check_opencv(self):
        """Check OpenCV"""
        try:
            import cv2
            self.opencv_status.config(text=f"📷 OpenCV: {cv2.__version__} ✅", fg='green')
            self.opencv_ok = True
        except ImportError:
            self.opencv_status.config(text="📷 OpenCV: Not installed ❌", fg='red')
            self.opencv_ok = False
        except Exception as e:
            self.opencv_status.config(text="📷 OpenCV: Error checking ❌", fg='red')
            self.opencv_ok = False
            
        self.root.after(100, self._check_mediapipe)
        
    def _check_mediapipe(self):
        """Check MediaPipe"""
        try:
            import mediapipe as mp
            self.mediapipe_status.config(text=f"🧠 MediaPipe: {mp.__version__} ✅", fg='green')
            self.mediapipe_ok = True
        except ImportError:
            self.mediapipe_status.config(text="🧠 MediaPipe: Not installed ❌", fg='red')
            self.mediapipe_ok = False
        except Exception as e:
            self.mediapipe_status.config(text="🧠 MediaPipe: Error loading ❌", fg='red')
            self.mediapipe_ok = False
            
        self.root.after(100, self._check_pyautogui)
        
    def _check_pyautogui(self):
        """Check PyAutoGUI"""
        try:
            import pyautogui
            self.pyautogui_status.config(text=f"🖱️ PyAutoGUI: {pyautogui.VERSION} ✅", fg='green')
            self.pyautogui_ok = True
        except ImportError:
            self.pyautogui_status.config(text="🖱️ PyAutoGUI: Not installed ❌", fg='red')
            self.pyautogui_ok = False
        except Exception as e:
            self.pyautogui_status.config(text="🖱️ PyAutoGUI: Error checking ❌", fg='red')
            self.pyautogui_ok = False
            
        self.root.after(100, self._check_gui)
        
    def _check_gui(self):
        """Check GUI libraries"""
        try:
            import matplotlib
            from PIL import Image
            self.gui_status.config(text="🖼️ GUI Libraries: Available ✅", fg='green')
            self.gui_ok = True
        except ImportError as e:
            self.gui_status.config(text=f"🖼️ GUI Libraries: Missing {str(e)} ❌", fg='red')
            self.gui_ok = False
        except Exception as e:
            self.gui_status.config(text="🖼️ GUI Libraries: Error checking ❌", fg='red')
            self.gui_ok = False
            
        self.root.after(100, self._update_recommendations)
        
    def _update_recommendations(self):
        """Update recommendations based on dependency check"""
        recommendations = []
        
        # Check what can be launched
        can_launch_advanced = (self.python_ok and self.opencv_ok and 
                              self.mediapipe_ok and self.pyautogui_ok and self.gui_ok)
        can_launch_simple = (self.python_ok and self.opencv_ok and 
                            self.pyautogui_ok and self.gui_ok)
        
        if can_launch_advanced:
            recommendations.append("✅ RECOMMENDED: Launch Advanced Version")
            recommendations.append("   - Full MediaPipe-based gesture recognition")
            recommendations.append("   - High accuracy hand tracking")
            recommendations.append("   - Advanced gesture analytics")
            self.advanced_button.config(state='normal')
            
        elif can_launch_simple:
            recommendations.append("⚠️ FALLBACK: Launch Simple Version")
            recommendations.append("   - Color-based hand tracking")
            recommendations.append("   - Basic gesture recognition")
            recommendations.append("   - Good for systems without MediaPipe")
            self.simple_button.config(state='normal')
        else:
            recommendations.append("❌ CANNOT LAUNCH: Missing critical dependencies")
            recommendations.append("   - Please install missing dependencies first")
            
        if not can_launch_advanced and not can_launch_simple:
            recommendations.append("")
            recommendations.append("📦 Required installations:")
            if not self.opencv_ok:
                recommendations.append("   - pip install opencv-python")
            if not self.pyautogui_ok:
                recommendations.append("   - pip install pyautogui")
            if not self.gui_ok:
                recommendations.append("   - pip install matplotlib pillow")
            if not self.mediapipe_ok:
                recommendations.append("   - pip install mediapipe (for advanced version)")
                
        # Update recommendation text
        self.recommendation_text.delete(1.0, tk.END)
        self.recommendation_text.insert(tk.END, "\n".join(recommendations))
        
    def launch_advanced(self):
        """Launch the advanced MediaPipe version"""
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'gesture_control_pro.py')
            if os.path.exists(script_path):
                subprocess.Popen([sys.executable, script_path])
                self.root.destroy()
            else:
                messagebox.showerror("Error", "gesture_control_pro.py not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch advanced version: {str(e)}")
            
    def launch_simple(self):
        """Launch the simple color tracking version"""
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'simple_tracking_pro.py')
            if os.path.exists(script_path):
                subprocess.Popen([sys.executable, script_path])
                self.root.destroy()
            else:
                messagebox.showerror("Error", "simple_tracking_pro.py not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch simple version: {str(e)}")
            
    def install_dependencies(self):
        """Install missing dependencies"""
        install_window = tk.Toplevel(self.root)
        install_window.title("📦 Dependency Installation")
        install_window.geometry("500x400")
        install_window.configure(bg='#2b2b2b')
        
        # Installation interface
        tk.Label(install_window, text="📦 Install Missing Dependencies",
                font=('Arial', 16, 'bold'), bg='#2b2b2b', fg='white').pack(pady=20)
        
        # Checkboxes for each dependency
        self.install_vars = {}
        
        deps_frame = tk.Frame(install_window, bg='#2b2b2b')
        deps_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        dependencies = [
            ('opencv-python', 'OpenCV for computer vision', not self.opencv_ok),
            ('mediapipe', 'MediaPipe for hand detection', not self.mediapipe_ok),
            ('pyautogui', 'PyAutoGUI for system control', not self.pyautogui_ok),
            ('matplotlib', 'Matplotlib for analytics', not self.gui_ok),
            ('pillow', 'PIL for image processing', not self.gui_ok),
            ('numpy', 'NumPy for numerical operations', True),
            ('scikit-learn', 'Scikit-learn for ML models', True)
        ]
        
        for package, description, should_check in dependencies:
            var = tk.BooleanVar(value=should_check)
            self.install_vars[package] = var
            
            cb = tk.Checkbutton(deps_frame, text=f"{package} - {description}",
                               variable=var, bg='#2b2b2b', fg='white',
                               selectcolor='#2b2b2b', activebackground='#2b2b2b',
                               activeforeground='white', font=('Arial', 10))
            cb.pack(anchor='w', pady=5)
        
        # Install button
        tk.Button(install_window, text="🚀 Install Selected",
                 command=lambda: self.run_installation(install_window),
                 bg='#00aa00', fg='white', font=('Arial', 12, 'bold'),
                 height=2).pack(pady=20)
        
    def run_installation(self, install_window):
        """Run the installation process"""
        packages_to_install = []
        for package, var in self.install_vars.items():
            if var.get():
                packages_to_install.append(package)
                
        if not packages_to_install:
            messagebox.showinfo("Info", "No packages selected for installation")
            return
            
        # Create progress window
        progress_window = tk.Toplevel(install_window)
        progress_window.title("Installing...")
        progress_window.geometry("400x200")
        progress_window.configure(bg='#2b2b2b')
        
        tk.Label(progress_window, text="Installing dependencies...",
                font=('Arial', 14, 'bold'), bg='#2b2b2b', fg='white').pack(pady=20)
        
        progress = ttk.Progressbar(progress_window, mode='indeterminate')
        progress.pack(fill='x', padx=20, pady=20)
        progress.start()
        
        status_label = tk.Label(progress_window, text="Starting installation...",
                               bg='#2b2b2b', fg='white')
        status_label.pack(pady=10)
        
        # Run installation in thread
        import threading
        def install_thread():
            try:
                for i, package in enumerate(packages_to_install):
                    status_label.config(text=f"Installing {package}...")
                    result = subprocess.run([sys.executable, '-m', 'pip', 'install', package],
                                          capture_output=True, text=True)
                    if result.returncode != 0:
                        messagebox.showerror("Error", f"Failed to install {package}:\n{result.stderr}")
                        
                progress.stop()
                progress_window.destroy()
                install_window.destroy()
                messagebox.showinfo("Success", "Dependencies installed! Please restart the launcher.")
                
            except Exception as e:
                progress.stop()
                progress_window.destroy()
                messagebox.showerror("Error", f"Installation failed: {str(e)}")
                
        threading.Thread(target=install_thread, daemon=True).start()
        
    def run(self):
        """Run the launcher"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        launcher = GestureLauncher()
        launcher.run()
    except Exception as e:
        print(f"Error starting launcher: {e}")

if __name__ == "__main__":
    main()
