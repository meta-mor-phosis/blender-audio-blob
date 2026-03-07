# Sound Reactive Blob (Blender + Python)

A real-time sound-reactive blob created in Blender using Python.

The blob deforms based on audio features:

Amplitude → Z-axis spikes  
Frequency → X-axis spikes  
Energy → Y-axis spikes  

## Requirements

- Blender 4+
- Python libraries:
  - pyaudio
  - numpy

## Running

1. Open `blob_project.blend`
2. Go to the scripting workspace
3. Run `scripts/sound_blob.py`
4. Play audio or speak into microphone
