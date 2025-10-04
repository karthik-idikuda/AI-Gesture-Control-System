#!/bin/bash

# Professional AI Gesture Control System - Enhanced Run Script
echo "🤖 Professional AI-Based Hand Gesture Control System v2.0"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    echo -e "${2}${1}${NC}"
}

# Check for virtual environment
if [ -d "venv_brew" ]; then
    PYTHON_CMD="venv_brew/bin/python"
    print_color "✅ Using virtual environment: venv_brew" $GREEN
elif [ -d "venv" ]; then
    PYTHON_CMD="venv/bin/python"
    print_color "✅ Using virtual environment: venv" $GREEN
else
    PYTHON_CMD="python3"
    print_color "⚠️ Using system Python (consider using virtual environment)" $YELLOW
fi

# Show menu
echo ""
print_color "🚀 LAUNCH OPTIONS:" $CYAN
print_color "1. 🎯 Advanced Version (MediaPipe-based)" $BLUE
print_color "2. 🎨 Simple Version (Color-based)" $BLUE
print_color "3. 🚀 Smart Launcher (Auto-detect)" $BLUE
print_color "4. 🎬 Interactive Demo" $PURPLE
print_color "5. 📜 Legacy Version" $YELLOW
print_color "6. ❌ Exit" $RED

echo ""
read -p "Select option (1-6): " choice

case $choice in
    1)
        print_color "🎯 Launching Advanced Version..." $GREEN
        if [ -f "gesture_control_pro.py" ]; then
            $PYTHON_CMD gesture_control_pro.py
        else
            print_color "❌ gesture_control_pro.py not found!" $RED
        fi
        ;;
    2)
        print_color "🎨 Launching Simple Version..." $GREEN
        if [ -f "simple_tracking_pro.py" ]; then
            $PYTHON_CMD simple_tracking_pro.py
        else
            print_color "❌ simple_tracking_pro.py not found!" $RED
        fi
        ;;
    3)
        print_color "🚀 Launching Smart Launcher..." $GREEN
        if [ -f "launcher.py" ]; then
            $PYTHON_CMD launcher.py
        else
            print_color "❌ launcher.py not found!" $RED
        fi
        ;;
    4)
        print_color "🎬 Starting Interactive Demo..." $PURPLE
        if [ -f "demo.py" ]; then
            $PYTHON_CMD demo.py
        else
            print_color "❌ demo.py not found!" $RED
        fi
        ;;
    5)
        print_color "📜 Launching Legacy Version..." $YELLOW
        if [ -f "main.py" ]; then
            $PYTHON_CMD main.py --debug
        else
            print_color "❌ main.py not found!" $RED
        fi
        ;;
    6)
        print_color "👋 Goodbye!" $GREEN
        exit 0
        ;;
    *)
        print_color "❌ Invalid option. Please select 1-6." $RED
        exit 1
        ;;
esac

echo ""
print_color "🎉 Thank you for using Professional AI Gesture Control System!" $GREEN
