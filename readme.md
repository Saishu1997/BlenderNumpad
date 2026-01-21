# Blender Remote Pro
A mobile-based numpad and macro deck for Blender using Python Flask and PyAutoGUI.

### Features
- Dual Mode: Toggle between Viewport Labels and Classic Numpad.
- Long-Press: Tap for view, Hold for opposite view.
- Sculpting Tools: Quick access to F (Size) and Shift+F (Strength).

### Installation
1. `pip install -r requirements.txt`
2. Run `python blender_remote.py`
3. Open the displayed IP address on your phone's browser.

A Quick "Checklist" for Your New Setup:

    Static IP: If your phone stops connecting tomorrow, your PC's IP address might have changed. Just run ipconfig again and update the URL on your phone.

    Keep it Open: You can leave the Python script running in the background while you work; it uses almost zero CPU until you actually press a button.

    Browser as App: Don't forget to use the "Add to Home Screen" trick on your phone to get rid of the browser bars and make it feel like a real native app.
