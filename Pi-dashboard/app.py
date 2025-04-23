# app.py

from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet
from pmu2sine import get_next_plot

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def emit_plots():
    while True:
        socketio.sleep(0.5)  # update every 500ms
        plot = get_next_plot()
        if plot is None:
            break
        socketio.emit('update_plot', {'image': plot})

@socketio.on('connect')
def on_connect():
    print('Client connected')
    socketio.start_background_task(emit_plots)

if __name__ == '__main__':
    socketio.run(app, debug=True)
