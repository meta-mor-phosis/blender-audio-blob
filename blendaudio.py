import bpy
import pyaudio
import numpy as np
import random

# ----- SETTINGS -----

AMP_SENS = 4.0
FREQ_SENS = 3.0
ENERGY_SENS = 3.0

SPIKE_COUNT = 40

CHUNK = 1024
RATE = 44100

# ----- OBJECT -----

obj = bpy.context.active_object
mesh = obj.data

x_group = obj.vertex_groups.get("xgroup")
y_group = obj.vertex_groups.get("ygroup")
z_group = obj.vertex_groups.get("zgroup")

base_vertices = [v.co.copy() for v in mesh.vertices]

# ----- BUILD VERTEX LISTS -----

x_vertices = []
y_vertices = []
z_vertices = []

for v in mesh.vertices:

    for g in v.groups:

        if x_group and g.group == x_group.index:
            x_vertices.append(v.index)

        if y_group and g.group == y_group.index:
            y_vertices.append(v.index)

        if z_group and g.group == z_group.index:
            z_vertices.append(v.index)


# ----- AUDIO -----

p = pyaudio.PyAudio()

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK
)

# ----- LOOP -----

def update_blob():

    data = np.frombuffer(
        stream.read(CHUNK, exception_on_overflow=False),
        dtype=np.int16
    )

    amplitude = np.linalg.norm(data) / 15000

    fft = np.fft.fft(data)
    freq = np.argmax(np.abs(fft[:len(fft)//2])) / 150

    energy = np.sum(np.abs(fft)) / 3e6

    # reset mesh
    for i, v in enumerate(mesh.vertices):
        v.co = base_vertices[i]

    # ----- X spikes (frequency) -----

    for vid in random.sample(x_vertices, min(SPIKE_COUNT, len(x_vertices))):

        v = mesh.vertices[vid]
        base = base_vertices[vid]

        spike = freq * FREQ_SENS

        v.co.x = base.x + spike


    # ----- Y spikes (energy) -----

    for vid in random.sample(y_vertices, min(SPIKE_COUNT, len(y_vertices))):

        v = mesh.vertices[vid]
        base = base_vertices[vid]

        spike = energy * ENERGY_SENS

        v.co.y = base.y + spike


    # ----- Z spikes (amplitude) -----

    for vid in random.sample(z_vertices, min(SPIKE_COUNT, len(z_vertices))):

        v = mesh.vertices[vid]
        base = base_vertices[vid]

        spike = amplitude * AMP_SENS

        v.co.z = base.z + spike


    mesh.update()

    return 0.05


bpy.app.timers.register(update_blob)