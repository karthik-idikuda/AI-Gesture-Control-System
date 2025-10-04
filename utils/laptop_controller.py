import pyautogui
import math
import time
import subprocess
import sys
import platform

# Set safety feature to prevent mouse from going to corners
pyautogui.FAILSAFE = True

class LaptopController:
    def __init__(self):
        """Initialize the laptop controller"""
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Current mouse position
        self.mouse_x, self.mouse_y = pyautogui.position()
        
        # Time of last action to prevent too frequent actions
        self.last_action_time = time.time()
        self.action_cooldown = 0.5  # seconds
        
        # Scroll and volume control sensitivity
        self.scroll_sensitivity = 5
        self.volume_sensitivity = 2
        
        # Current system
        self.system = platform.system()
        
    def move_mouse(self, x_normalized, y_normalized, smooth=True):
        """
        Move mouse cursor based on normalized coordinates (0.0 to 1.0)
        
        Args:
            x_normalized: Normalized x-coordinate (0.0 to 1.0)
            y_normalized: Normalized y-coordinate (0.0 to 1.0)
            smooth: Whether to move the mouse smoothly
        """
        # Calculate absolute screen position
        x_screen = int(x_normalized * self.screen_width)
        y_screen = int(y_normalized * self.screen_height)
        
        # Ensure coordinates are within screen bounds
        x_screen = max(0, min(x_screen, self.screen_width - 1))
        y_screen = max(0, min(y_screen, self.screen_height - 1))
        
        # Move mouse
        if smooth:
            pyautogui.moveTo(x_screen, y_screen, duration=0.1)
        else:
            pyautogui.moveTo(x_screen, y_screen)
            
        self.mouse_x, self.mouse_y = x_screen, y_screen
        
    def click(self, button='left', double=False):
        """
        Perform mouse click
        
        Args:
            button: Mouse button to click ('left', 'right', 'middle')
            double: Whether to double-click
        """
        if time.time() - self.last_action_time < self.action_cooldown:
            return
            
        if double:
            pyautogui.doubleClick(button=button)
        else:
            pyautogui.click(button=button)
            
        self.last_action_time = time.time()
        
    def right_click(self):
        """Perform right click"""
        self.click(button='right')
        
    def drag(self, x_normalized, y_normalized, smooth=True):
        """
        Perform drag operation
        
        Args:
            x_normalized: Normalized x-coordinate (0.0 to 1.0)
            y_normalized: Normalized y-coordinate (0.0 to 1.0)
            smooth: Whether to move the mouse smoothly
        """
        # Calculate absolute screen position
        x_screen = int(x_normalized * self.screen_width)
        y_screen = int(y_normalized * self.screen_height)
        
        # Ensure coordinates are within screen bounds
        x_screen = max(0, min(x_screen, self.screen_width - 1))
        y_screen = max(0, min(y_screen, self.screen_height - 1))
        
        # Drag mouse to position
        if smooth:
            pyautogui.dragTo(x_screen, y_screen, duration=0.1)
        else:
            pyautogui.dragTo(x_screen, y_screen)
            
        self.mouse_x, self.mouse_y = x_screen, y_screen
        
    def scroll(self, direction, amount=None):
        """
        Scroll up or down
        
        Args:
            direction: 'up' or 'down'
            amount: Scroll amount (if None, uses default sensitivity)
        """
        if time.time() - self.last_action_time < self.action_cooldown / 2:
            return
            
        scroll_amount = amount if amount is not None else self.scroll_sensitivity
        
        if direction == 'up':
            pyautogui.scroll(scroll_amount)
        elif direction == 'down':
            pyautogui.scroll(-scroll_amount)
            
        self.last_action_time = time.time()
        
    def adjust_volume(self, direction):
        """
        Adjust system volume
        
        Args:
            direction: 'up' or 'down'
        """
        if time.time() - self.last_action_time < self.action_cooldown:
            return
            
        # Different commands based on OS
        if self.system == 'Darwin':  # macOS
            vol_adjust = self.volume_sensitivity
            if direction == 'down':
                vol_adjust = -vol_adjust
                
            # Adjust volume using osascript
            cmd = f"osascript -e 'set volume output volume (output volume of (get volume settings) + {vol_adjust})'"
            subprocess.run(cmd, shell=True)
            
        elif self.system == 'Windows':
            key = 'volumeup' if direction == 'up' else 'volumedown'
            pyautogui.press(key, presses=self.volume_sensitivity)
            
        elif self.system == 'Linux':
            vol_adjust = self.volume_sensitivity
            if direction == 'down':
                vol_adjust = -vol_adjust
                
            try:
                if vol_adjust > 0:
                    subprocess.run(['amixer', '-q', 'sset', 'Master', f'{vol_adjust}%+'])
                else:
                    subprocess.run(['amixer', '-q', 'sset', 'Master', f'{-vol_adjust}%-'])
            except:
                pass
                
        self.last_action_time = time.time()
        
    def brightness_control(self, direction):
        """
        Adjust screen brightness
        
        Args:
            direction: 'up' or 'down'
        """
        if time.time() - self.last_action_time < self.action_cooldown:
            return
            
        # Different approaches based on OS
        if self.system == 'Darwin':  # macOS
            key = 'f2' if direction == 'up' else 'f1'
            pyautogui.keyDown('fn')
            pyautogui.press(key)
            pyautogui.keyUp('fn')
            
        elif self.system == 'Windows':
            key = 'brightnessup' if direction == 'up' else 'brightnessdown'
            pyautogui.press(key)
            
        self.last_action_time = time.time()
        
    def press_key(self, key):
        """
        Press a keyboard key
        
        Args:
            key: Key to press
        """
        pyautogui.press(key)
        
    def key_combination(self, keys):
        """
        Press a combination of keys
        
        Args:
            keys: List of keys to press together
        """
        pyautogui.hotkey(*keys)
        
    def media_control(self, action):
        """
        Control media playback
        
        Args:
            action: 'play', 'pause', 'next', 'previous'
        """
        if time.time() - self.last_action_time < self.action_cooldown:
            return
            
        if self.system == 'Darwin':  # macOS
            key_map = {
                'play': 'playpause',
                'pause': 'playpause',
                'next': 'nexttrack',
                'previous': 'prevtrack'
            }
        else:
            key_map = {
                'play': 'playpause',
                'pause': 'playpause',
                'next': 'nexttrack',
                'previous': 'prevtrack'
            }
            
        key = key_map.get(action.lower())
        if key:
            pyautogui.press(key)
            
        self.last_action_time = time.time()
