from flask import Flask, render_template, request, send_file
import webbrowser
import threading
import os
from datetime import datetime, timedelta
import time
from PIL import Image
import base64

app = Flask(__name__)

# Global variables
timer_running = False
start_time = None
elapsed_time = 0
input_file = None
adjust_mode = "Add"  # Default to Add

# Load and encode logo images
with open("logo.png", "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read()).decode('utf-8')

with open("logo2.png", "rb") as image_file:
    encoded_logo2 = base64.b64encode(image_file.read()).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html', timer=elapsed_time, selected_file=input_file, adjust_mode=adjust_mode, logo_image=encoded_logo, logo2_image=encoded_logo2)

@app.route('/start_timer', methods=['POST'])
def start_timer():
    global timer_running, start_time, elapsed_time
    if not timer_running:
        start_time = datetime.now()
        timer_running = True
        # Start a background thread to update the timer
        threading.Thread(target=update_timer, daemon=True).start()
    return {"status": "Timer started"}

def update_timer():
    global elapsed_time, timer_running
    while timer_running:
        elapsed_time = (datetime.now() - start_time).total_seconds()
        time.sleep(0.01)  # Update every 10ms

@app.route('/stop_timer', methods=['POST'])
def stop_timer():
    global timer_running, elapsed_time
    if timer_running:
        timer_running = False
        elapsed = elapsed_time
        if adjust_mode == "Subtract":
            elapsed = -elapsed
        return {"elapsed": elapsed}  # Return the raw value to preserve sign
    return {"elapsed": elapsed_time}

@app.route('/reset_timer', methods=['POST'])
def reset_timer():
    global timer_running, elapsed_time, start_time, input_file, adjust_mode
    timer_running = False
    elapsed_time = 0
    start_time = None
    input_file = None  # Reset the selected file
    adjust_mode = "Add"  # Reset adjust mode to Add
    return {"status": "Timer reset", "elapsed": 0, "selected_file": None, "adjust_mode": "Add"}

@app.route('/set_adjust_mode', methods=['POST'])
def set_adjust_mode():
    global adjust_mode
    adjust_mode = request.form.get('adjust_mode', 'Add')
    return {"status": "Mode set", "mode": adjust_mode}

@app.route('/upload', methods=['POST'])
def upload_file():
    global input_file
    file = request.files['file']
    if file and file.filename.endswith('.srt'):
        input_file = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(input_file)
        return {"status": "File uploaded successfully", "filename": file.filename}
    return {"status": "Invalid file, please upload an .srt file"}, 400

def parse_time(time_str):
    try:
        time_obj = datetime.strptime(time_str, "%H:%M:%S,%f")
        return time_obj
    except ValueError:
        time_obj = datetime.strptime(time_str, "%H:%M:%S")
        return time_obj.replace(microsecond=0)

def format_time(time_obj):
    return time_obj.strftime("%H:%M:%S,%f")[:-3]

@app.route('/adjust', methods=['POST'])
def adjust():
    global input_file, adjust_mode
    if not input_file:
        return {"status": "No file selected"}, 400

    seconds = float(request.form.get('seconds', 0))
    # Use adjust_mode to determine sign
    if adjust_mode == "Subtract":
        seconds = -abs(seconds)
    else:
        seconds = abs(seconds)
    output_filename = "adjusted_" + os.path.basename(input_file)
    output_file = os.path.join("uploads", output_filename)

    encodings = ['utf-8', 'cp1252', 'latin1']
    lines = None
    for encoding in encodings:
        try:
            with open(input_file, 'r', encoding=encoding) as f:
                lines = f.readlines()
            break
        except Exception:
            continue

    if lines is None:
        return {"status": "Failed to read file: Unsupported encoding"}, 400

    time_shift = timedelta(seconds=seconds)
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            new_lines.append(line + '\n')
            i += 1
            continue
        if line.isdigit():
            new_lines.append(line + '\n')
            i += 1
            if i < len(lines):
                timing_line = lines[i].strip()
                if '-->' in timing_line:
                    try:
                        start_time, end_time = timing_line.split(' --> ')
                        start = parse_time(start_time)
                        end = parse_time(end_time)

                        # Ensure subtraction works correctly
                        if seconds < 0:
                            # For negative shifts, ensure timestamps don't go below 0
                            shifted_start = start + time_shift
                            shifted_end = end + time_shift
                            if shifted_start < datetime.strptime("00:00:00,000", "%H:%M:%S,%f"):
                                shifted_start = datetime.strptime("00:00:00,000", "%H:%M:%S,%f")
                            if shifted_end < datetime.strptime("00:00:00,000", "%H:%M:%S,%f"):
                                shifted_end = datetime.strptime("00:00:00,000", "%H:%M:%S,%f")
                            start = shifted_start
                            end = shifted_end
                        else:
                            start = start + time_shift
                            end = end + time_shift

                        new_timing = f"{format_time(start)} --> {format_time(end)}\n"
                        new_lines.append(new_timing)
                    except Exception as e:
                        return {"status": f"Invalid time format: {e}"}, 400
                i += 1
        else:
            new_lines.append(line + '\n')
            i += 1

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return send_file(output_file, as_attachment=True, download_name=output_filename)
    except Exception as e:
        return {"status": f"Failed to save file: {e}"}, 400

@app.route('/get_timer', methods=['GET'])
def get_timer():
    global elapsed_time, timer_running, start_time
    if timer_running:
        current_elapsed = (datetime.now() - start_time).total_seconds()
    else:
        current_elapsed = elapsed_time
    return {"elapsed": round(current_elapsed, 3)}

def open_browser():
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)