from flask import Flask, render_template, jsonify
import pyaudio
import numpy as np
import threading
import time

app = Flask(__name__)

# Initialize variables for messages
messages = {
    'message': '',
    'message2': '',
    'message3': ''
}

# Function to detect sound
def generate_cake_svg(show_flames=True):
    svg_code = """
    <svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
        <!-- Draw the cake -->
        <rect x="40" y="90" width="120" height="20" fill="yellow"/>
        <rect x="40" y="110" width="120" height="60" fill="brown"/>
    """
    if show_flames:
        for x in range(60, 150, 20):
            svg_code += f"""
            <line x1="{x}" y1="90" x2="{x}" y2="70" stroke="black" stroke-width="3"/>
            <circle cx="{x}" cy="65" r="4" fill="red" class="flame"/>
            """
    svg_code += "</svg>"
    return svg_code

# Function to detect sound
def detect_sound():
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    # Read microphone input and calculate average amplitude
    data = np.frombuffer(stream.read(1024), dtype=np.int16)
    amplitude = np.mean(np.abs(data))
    print(amplitude)

    # Close the audio stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    return amplitude > 30  # Adjust this threshold as needed

@app.route('/')
def birthday_card():
    # Generate SVG code for cake with candles
    cake_svg = generate_cake_svg(show_flames=True)

    # Thread to display message and detect sound simultaneously
    def display_message_and_detect_sound():
        time.sleep(3)
        sound_detected = detect_sound()
        if sound_detected:
            messages['message'] = "Here you go:"

        if not sound_detected:
            messages['message2'] = "Literally blow in the screen. No kidding"
            time.sleep(4)
            sound_detected = detect_sound()

            if sound_detected:
                messages['message'] = "Here you go:"

            if not sound_detected:
                time.sleep(3)
                messages['message3'] = "Well... someone is in need of breathing practices. Take it for free"
                messages['message'] = "Here you go:"

    # Start the thread
    threading.Thread(target=display_message_and_detect_sound).start()

    # Return HTML template with SVG code and messages
    return render_template('index.html', cake_svg=cake_svg, messages=messages)

@app.route('/get_messages')
def get_messages():
    # Return messages as JSON data
    return jsonify(messages)

@app.route('/letter')
def get_letter():
    return render_template('letter.html')

if __name__ == '__main__':
    app.run(debug=True)