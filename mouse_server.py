from flask import Flask, Response, request, send_from_directory
import cv2
import mss
import numpy as np
import pyautogui
import os

app = Flask(__name__)

# Screen capture setup
sct = mss.mss()
monitor = sct.monitors[1]  # Use the first monitor; change as necessary

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

# Video streaming generator
def generate_frames():
    while True:
        # Capture the screen
        img = sct.grab(monitor)
        # Convert to a format OpenCV can work with
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)  # Convert BGRA to BGR

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in a format suitable for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/move', methods=['POST'])
def move_mouse():
    x = request.form.get('x', type=float)
    y = request.form.get('y', type=float)

    # Move the mouse to the specified coordinates
    pyautogui.moveRel(x, y)  # Relative movement based on input
    return "Mouse moved", 200

@app.route('/left_click', methods=['POST'])
def left_click():
    # Perform a left click
    pyautogui.click()
    return "Left Clicked", 200

@app.route('/right_click', methods=['POST'])
def right_click():
    # Perform a right click
    pyautogui.click(button='right')
    return "Right Clicked", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
