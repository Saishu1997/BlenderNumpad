from flask import Flask
import pyautogui

pyautogui.PAUSE = 0
app = Flask(__name__)

HTML_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Blender Remote Pro</title>
    <style>
        body { 
            background: #1a1a1a; color: #eee; font-family: 'Segoe UI', sans-serif; 
            margin: 0; display: flex; flex-direction: column; align-items: center; 
            height: 100vh; overflow: hidden; user-select: none;
        }
        
        .tabs { display: flex; width: 100%; background: #252525; border-bottom: 1px solid #444; }
        .tab { flex: 1; padding: 15px; text-align: center; color: #888; font-weight: bold; }
        .tab.active { color: #3d7cc9; border-bottom: 3px solid #3d7cc9; background: #2a2a2a; }

        .container { flex: 1; width: 100%; display: none; flex-direction: column; align-items: center; justify-content: center; padding: 10px; box-sizing: border-box;}
        .container.active { display: flex; }

        .header { margin: 5px 0 15px 0; font-size: 0.8rem; color: #888; display: flex; align-items: center; gap: 10px; }

        .numpad-wrapper { display: flex; gap: 10px; align-items: stretch; }
        .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; width: 100%; max-width: 380px;}
        .operators { display: flex; flex-direction: column; gap: 10px; }

        button { 
            background: #2a2a2a; color: #fff; border: 1px solid #3d3d3d; padding: 18px; 
            font-size: 0.95rem; border-radius: 10px; touch-action: manipulation; transition: 0.1s;
        }
        .op-btn { background: #333; color: #3d7cc9; font-weight: bold; }
        button:active { background: #444; transform: scale(0.95); }
        
        .axis-z { border-bottom: 4px solid #3d7cc9; }
        .axis-x { border-bottom: 4px solid #c93d3d; }
        .axis-y { border-bottom: 4px solid #53a749; }
        
        .sculpt-btn { background: #2d3e2d; border-color: #53a749; }
        .display-btn { background: #2d2d3e; border-color: #6a6ad4; }
        .mode-btn { color:#e5ad24; font-weight: bold; }

        .switch { position: relative; display: inline-block; width: 40px; height: 20px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background: #444; border-radius: 20px; transition: .3s; }
        .slider:before { position: absolute; content: ""; height: 14px; width: 14px; left: 3px; bottom: 3px; background: white; transition: .3s; border-radius: 50%; }
        input:checked + .slider { background: #3d7cc9; }
        input:checked + .slider:before { transform: translateX(20px); }
        
        h4 { margin: 10px 0 5px 0; color: #666; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }
    </style>
</head>
<body>

    <div class="tabs">
        <div class="tab active" onclick="openTab('view-tab')">VIEW</div>
        <div class="tab" onclick="openTab('tools-tab')">TOOLS</div>
    </div>

    <div id="view-tab" class="container active">
        <div class="header">
            <span>Labels</span>
            <label class="switch"><input type="checkbox" id="modeToggle" onchange="toggleLabels()"><span class="slider"></span></label>
            <span>Numbers</span>
        </div>
        <div class="numpad-wrapper">
            <div class="grid">
                <button class="axis-z" id="num7" data-blender="Top" data-classic="7" ontouchstart="hS(event,'num7')" ontouchend="hE(event,'num7')">Top</button>
                <button id="num8" data-blender="Up" data-classic="8" ontouchstart="hS(event,'num8')" ontouchend="hE(event,'num8')">Up</button>
                <button id="num9" data-blender="Persp" data-classic="9" ontouchstart="hS(event,'num9')" ontouchend="hE(event,'num9')">Persp</button>
                <button class="axis-x" id="num4" data-blender="Left" data-classic="4" ontouchstart="hS(event,'num4')" ontouchend="hE(event,'num4')">Left</button>
                <button id="num5" data-blender="Ortho" data-classic="5" ontouchstart="hS(event,'num5')" ontouchend="hE(event,'num5')">Ortho</button>
                <button class="axis-x" id="num6" data-blender="Right" data-classic="6" ontouchstart="hS(event,'num6')" ontouchend="hE(event,'num6')">Right</button>
                <button class="axis-y" id="num1" data-blender="Front" data-classic="1" ontouchstart="hS(event,'num1')" ontouchend="hE(event,'num1')">Front</button>
                <button id="num2" data-blender="Down" data-classic="2" ontouchstart="hS(event,'num2')" ontouchend="hE(event,'num2')">Down</button>
                <button class="axis-y" id="num3" data-blender="Back" data-classic="3" ontouchstart="hS(event,'num3')" ontouchend="hE(event,'num3')">Back</button>
                <button id="num0" data-blender="Cam" data-classic="0" ontouchstart="hS(event,'num0')" ontouchend="hE(event,'num0')">Cam</button>
                <button id="decimal" data-blender="Focus" data-classic="." ontouchstart="hS(event,'decimal')" ontouchend="hE(event,'decimal')">Focus</button>
                <button id="enter" style="background:#3d7cc9" onclick="send('enter')">Enter</button>
            </div>
            <div class="operators">
                <button class="op-btn" onclick="send('multiply')">*</button>
                <button class="op-btn" onclick="send('subtract')">-</button>
                <button class="op-btn" onclick="send('add')">+</button>
                <button class="op-btn" onclick="send('divide')">/</button>
            </div>
        </div>
    </div>

    <div id="tools-tab" class="container">
        <h4>Transform</h4>
        <div class="grid">
            <button onclick="send('g')">Move (G)</button>
            <button onclick="send('r')">Rotate (R)</button>
            <button onclick="send('s')">Scale (S)</button>
        </div>
        
        <h4>Sculpt & Selection</h4>
        <div class="grid">
            <button class="sculpt-btn" onclick="send('f')">Size (F)</button>
            <button class="sculpt-btn" onclick="send('shift+f')">Strength</button>
            <button class="sculpt-btn" onclick="send('ctrl+z')">Undo</button>
            <button onclick="send('a')">All (A)</button>
            <button onclick="send('alt+a')">None</button>
            <button class="mode-btn" onclick="send('tab')">TAB</button>
        </div>

        <h4>Display & View</h4>
        <div class="grid">
            <button class="display-btn" onclick="send('shift+z')">Wireframe</button>
            <button class="display-btn" onclick="send('alt+shift+z')">Overlays</button>
            <button class="mode-btn" onclick="send('z')">Shading</button>
        </div>
    </div>

    <script>
        let timer;
        let isLongPress = false;

        function openTab(tabId) {
            document.querySelectorAll('.container').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }

        function hS(e, k) {
            e.preventDefault(); isLongPress = false;
            timer = setTimeout(() => {
                isLongPress = true; send('ctrl+' + k);
                if (navigator.vibrate) navigator.vibrate([40, 30, 40]);
            }, 500);
        }

        function hE(e, k) {
            e.preventDefault(); clearTimeout(timer);
            if (!isLongPress) { send(k); if (navigator.vibrate) navigator.vibrate(20); }
        }

        function send(key) { fetch('/keypress/' + key); }

        function toggleLabels() {
            const isClassic = document.getElementById('modeToggle').checked;
            document.querySelectorAll('#view-tab .grid button').forEach(btn => {
                if(btn.id !== 'enter') {
                    btn.innerText = isClassic ? btn.getAttribute('data-classic') : btn.getAttribute('data-blender');
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return HTML_UI

@app.route('/keypress/<key>')
def press_key(key):
    try:
        mapping = {'add': 'add', 'subtract': 'subtract', 'multiply': 'multiply', 'divide': 'divide', 'enter': 'enter', 'decimal': 'decimal'}
        
        if '+' in key and 'ctrl+' not in key and 'alt+' not in key and 'shift+' not in key:
            # Handle generic combo if we ever add more
            parts = key.split('+')
            pyautogui.hotkey(*parts)
        elif 'ctrl+' in key:
            # Handles double modifiers like alt+shift+z
            mods = key.split('+')
            pyautogui.hotkey(*mods)
        elif 'alt+' in key:
            mods = key.split('+')
            pyautogui.hotkey(*mods)
        elif 'shift+' in key:
            mods = key.split('+')
            pyautogui.hotkey(*mods)
        else:
            pyautogui.press(mapping.get(key, key))
            
        print(f"Sent: {key}")
    except Exception as e:
        print(f"Error: {e}")
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)