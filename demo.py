#!/usr/bin/env python3
"""
Professional Gesture Control Demo
=================================
Interactive demo showcasing all features of the Professional AI-Based
Hand Gesture Control System.
"""

import sys
import os
import time
import subprocess

def print_header():
    """Print professional demo header"""
    print("\n" + "="*70)
    print("🤖 PROFESSIONAL AI-BASED HAND GESTURE CONTROL SYSTEM v2.0")
    print("="*70)
    print("Enterprise-grade gesture recognition with advanced analytics")
    print("Developed by: Professional AI Development Team")
    print("="*70)

def print_features():
    """Print key features"""
    print("\n✨ KEY FEATURES:")
    print("  🎯 Real-time MediaPipe hand detection (95%+ accuracy)")
    print("  🖥️ Professional dark-themed GUI with live analytics")
    print("  📊 Performance monitoring and gesture statistics")
    print("  🎮 Complete laptop control (mouse, keyboard, system)")
    print("  🔧 Dual-mode operation (Advanced + Simple fallback)")
    print("  ⚙️ Customizable settings and gesture mappings")
    print("  📈 Interactive charts and real-time metrics")
    print("  🎛️ HSV calibration tools for color tracking")

def print_gesture_table():
    """Print supported gestures"""
    print("\n🎮 SUPPORTED GESTURES:")
    print("  ┌─────────────────┬─────────────────┬─────────────────────┐")
    print("  │ Gesture         │ Advanced Ver.   │ Action              │")
    print("  ├─────────────────┼─────────────────┼─────────────────────┤")
    print("  │ 👉 Point        │ ✅ High Accuracy │ Move cursor         │")
    print("  │ ✊ Fist          │ ✅ Reliable      │ Left click          │")
    print("  │ ✋ Open Palm     │ ✅ Smooth        │ Scroll up/down      │")
    print("  │ ✌️ Victory       │ ✅ Accurate      │ Right click         │")
    print("  │ 👍 Thumbs Up    │ ✅ Detected      │ Volume up           │")
    print("  │ 👎 Thumbs Down  │ ✅ Detected      │ Volume down         │")
    print("  │ 🤏 Pinch        │ ✅ Precise       │ Drag/drop items     │")
    print("  │ 👌 OK Sign      │ ✅ Advanced      │ Brightness control  │")
    print("  └─────────────────┴─────────────────┴─────────────────────┘")

def check_system():
    """Check system capabilities"""
    print("\n🔍 SYSTEM ANALYSIS:")
    
    # Check Python
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"  🐍 Python: {python_version}", end="")
    if sys.version_info >= (3, 7):
        print(" ✅")
    else:
        print(" ❌ (Need 3.7+)")
    
    # Check dependencies
    deps = {
        'cv2': '📷 OpenCV',
        'mediapipe': '🧠 MediaPipe', 
        'pyautogui': '🖱️ PyAutoGUI',
        'matplotlib': '📊 Matplotlib',
        'PIL': '🖼️ PIL',
        'numpy': '🔢 NumPy'
    }
    
    available_deps = []
    missing_deps = []
    
    for module, name in deps.items():
        try:
            __import__(module)
            print(f"  {name}: Available ✅")
            available_deps.append(module)
        except ImportError:
            print(f"  {name}: Missing ❌")
            missing_deps.append(module)
    
    return len(available_deps), len(missing_deps)

def show_demo_options():
    """Show available demo options"""
    print("\n🚀 AVAILABLE APPLICATIONS:")
    print("  1. 🎯 Advanced Version (gesture_control_pro.py)")
    print("     - Full MediaPipe-based detection")
    print("     - Professional GUI with analytics")
    print("     - Real-time performance monitoring")
    print("     - Advanced gesture recognition")
    
    print("\n  2. 🎨 Simple Version (simple_tracking_pro.py)")
    print("     - Color-based hand tracking")
    print("     - HSV calibration interface")
    print("     - Lightweight operation")
    print("     - Good for systems without MediaPipe")
    
    print("\n  3. 🚀 Smart Launcher (launcher.py)")
    print("     - Automatic dependency checking")
    print("     - Intelligent version selection")
    print("     - Installation assistance")
    print("     - System recommendations")

def interactive_menu():
    """Interactive demo menu"""
    while True:
        print("\n" + "─"*50)
        print("📋 DEMO MENU:")
        print("  1. 🎯 Launch Advanced Version")
        print("  2. 🎨 Launch Simple Version") 
        print("  3. 🚀 Launch Smart Launcher")
        print("  4. 📊 Run System Check")
        print("  5. 📖 View Documentation")
        print("  6. 🔧 View Project Structure")
        print("  7. ❌ Exit Demo")
        print("─"*50)
        
        try:
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == '1':
                launch_advanced()
            elif choice == '2':
                launch_simple()
            elif choice == '3':
                launch_launcher()
            elif choice == '4':
                run_system_check()
            elif choice == '5':
                view_documentation()
            elif choice == '6':
                view_project_structure()
            elif choice == '7':
                print("\n👋 Thank you for trying the Professional Gesture Control System!")
                print("🔗 For more information, visit our documentation.")
                break
            else:
                print("❌ Invalid option. Please select 1-7.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def launch_advanced():
    """Launch advanced version"""
    print("\n🎯 Launching Advanced Version...")
    script_path = 'gesture_control_pro.py'
    if os.path.exists(script_path):
        try:
            # Check if we have the right Python executable
            python_exe = 'venv_brew/bin/python' if os.path.exists('venv_brew/bin/python') else sys.executable
            subprocess.Popen([python_exe, script_path])
            print("✅ Advanced version launched successfully!")
            print("📝 Check the new window for the professional interface.")
        except Exception as e:
            print(f"❌ Error launching advanced version: {e}")
    else:
        print(f"❌ File not found: {script_path}")

def launch_simple():
    """Launch simple version"""
    print("\n🎨 Launching Simple Version...")
    script_path = 'simple_tracking_pro.py'
    if os.path.exists(script_path):
        try:
            python_exe = 'venv_brew/bin/python' if os.path.exists('venv_brew/bin/python') else sys.executable
            subprocess.Popen([python_exe, script_path])
            print("✅ Simple version launched successfully!")
            print("📝 Check the new window for the color tracking interface.")
        except Exception as e:
            print(f"❌ Error launching simple version: {e}")
    else:
        print(f"❌ File not found: {script_path}")

def launch_launcher():
    """Launch smart launcher"""
    print("\n🚀 Launching Smart Launcher...")
    script_path = 'launcher.py'
    if os.path.exists(script_path):
        try:
            python_exe = 'venv_brew/bin/python' if os.path.exists('venv_brew/bin/python') else sys.executable
            subprocess.Popen([python_exe, script_path])
            print("✅ Smart launcher opened successfully!")
            print("📝 The launcher will help you choose the best version.")
        except Exception as e:
            print(f"❌ Error launching smart launcher: {e}")
    else:
        print(f"❌ File not found: {script_path}")

def run_system_check():
    """Run detailed system check"""
    print("\n🔍 Running Detailed System Check...")
    available, missing = check_system()
    
    print(f"\n📊 SUMMARY:")
    print(f"  ✅ Available dependencies: {available}")
    print(f"  ❌ Missing dependencies: {missing}")
    
    if missing == 0:
        print("  🎉 All dependencies available! You can use all features.")
        print("  💡 Recommendation: Use Advanced Version")
    elif available >= 3:
        print("  ⚠️ Some dependencies missing, but basic features available.")
        print("  💡 Recommendation: Use Simple Version or install missing deps")
    else:
        print("  ❌ Too many dependencies missing.")
        print("  💡 Recommendation: Run setup script or use Smart Launcher")

def view_documentation():
    """View documentation"""
    print("\n📖 DOCUMENTATION:")
    print("  📋 README_Pro.md - Comprehensive documentation")
    print("  📋 README.md - Original documentation")
    print("  📝 Code files contain detailed docstrings")
    
    if os.path.exists('README_Pro.md'):
        print("\n📄 Quick overview from README_Pro.md:")
        with open('README_Pro.md', 'r') as f:
            lines = f.readlines()[:20]  # First 20 lines
            for line in lines:
                if line.strip():
                    print("  " + line.strip())
    else:
        print("❌ Documentation files not found")

def view_project_structure():
    """View project structure"""
    print("\n🏗️ PROJECT STRUCTURE:")
    print("  gesture-control/")
    print("  ├── 🚀 launcher.py                    # Smart launcher")
    print("  ├── 🎯 gesture_control_pro.py         # Advanced version")  
    print("  ├── 🎨 simple_tracking_pro.py         # Simple version")
    print("  ├── 📜 main.py                        # Legacy version")
    print("  ├── 🔧 setup.sh                       # Setup script")
    print("  ├── 📋 requirements.txt               # Dependencies")
    print("  ├── utils/                            # Core modules")
    print("  │   ├── hand_detector.py             # MediaPipe detection")
    print("  │   ├── gesture_recognizer.py        # ML recognition")
    print("  │   ├── laptop_controller.py         # System control")
    print("  │   └── gesture_mapper.py            # Gesture mapping")
    print("  ├── data/                            # Training data")
    print("  ├── models/                          # ML models")
    print("  └── README_Pro.md                    # Documentation")
    
    print("\n📁 Current directory contents:")
    try:
        files = os.listdir('.')
        for file in sorted(files):
            if file.endswith('.py'):
                print(f"  🐍 {file}")
            elif file.endswith('.md'):
                print(f"  📄 {file}")
            elif file.endswith('.sh'):
                print(f"  🔧 {file}")
            elif os.path.isdir(file) and not file.startswith('.'):
                print(f"  📁 {file}/")
    except Exception as e:
        print(f"❌ Error reading directory: {e}")

def main():
    """Main demo function"""
    print_header()
    print_features()
    print_gesture_table()
    
    print("\n🔍 Checking system capabilities...")
    time.sleep(1)
    available, missing = check_system()
    
    if missing == 0:
        print("\n🎉 Perfect! All dependencies are available.")
        print("💡 You can use all advanced features.")
    elif available >= 3:
        print("\n⚠️ Good! Most dependencies available.")
        print("💡 You can use basic features or install missing ones.")
    else:
        print("\n❌ Several dependencies are missing.")
        print("💡 Please run the setup script or use the Smart Launcher.")
    
    show_demo_options()
    
    print("\n🎬 DEMO MODE ACTIVATED")
    interactive_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Please check your installation and try again.")
