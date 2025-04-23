# graph_generator.py

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

df = pd.read_csv('Bus2_Competition_Data.csv', usecols=['BUS2_VA_ANG', 'BUS2_VA_MAG', 'BUS2_Freq'])

T0 = 0
TE = 0.033
PI = np.pi
TIMERES = 1000
ts = np.linspace(T0, TE, TIMERES)

ROW = 0

def waveConditioning(mag, freq, ang):
    ys = np.sin((2*PI*freq*ts)+(ang*(PI/180)))
    ys = ys * mag * (128 / 229173.491)
    ys = ys + 128
    return ys.astype(int)

def get_next_plot():
    global ROW
    if ROW >= len(df):
        return None  # End of data

    ang = df.iat[ROW, 0]
    mag = df.iat[ROW, 1]
    freq = df.iat[ROW, 2]

    ys = waveConditioning(mag, freq, ang)
    fig, ax = plt.subplots()
    ax.plot(ts, ys)
    ax.set_title(f"Row {ROW}: F={freq:.2f}Hz, MAG={mag:.2f}, ANG={ang:.2f}")

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    ROW += 1
    return image_base64
