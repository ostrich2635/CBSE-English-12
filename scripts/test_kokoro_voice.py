import os
import wave
import numpy as np
from kokoro_onnx import Kokoro
import subprocess

model_dir = r"c:\Users\aishw\Downloads\CBSE Eng\audio\kokoro_model"
model_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
voices_path = os.path.join(model_dir, "voices.bin")

out_dir = r"c:\Users\aishw\Downloads\CBSE Eng\audio\test_tones"
os.makedirs(out_dir, exist_ok=True)

test_text = "“When I leave,” Sophie said, coming home from school, “I’m going to have a boutique.” Jansie, linking arms with her along the street, looked doubtful. “Takes money, Soaf, something like that.” “I’ll find it,” Sophie said, staring far down the street."

def save_wav(filename, samples, sample_rate):
    if samples.dtype != np.int16:
        samples = np.clip(samples, -1.0, 1.0)
        samples = (samples * 32767).astype(np.int16)
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2) # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(samples.tobytes())

def test():
    print("Loading Kokoro ONNX model...")
    kokoro = Kokoro(model_path, voices_path)
    
    # Test bm_george (British male narrator - warm baritone)
    print("Generating with bm_george (British male)...")
    samples, sr = kokoro.create(test_text, voice="bm_george", speed=0.92, lang="en-gb")
    wav_path = os.path.join(out_dir, "kokoro_george.wav")
    save_wav(wav_path, samples, sr)
    
    # Convert to mp3
    mp3_path = os.path.join(out_dir, "kokoro_george.mp3")
    subprocess.run(["ffmpeg", "-i", wav_path, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_path, "-y"], capture_output=True)
    print(f"✓ Saved {mp3_path} ({os.path.getsize(mp3_path) / 1024:.1f} KB)")

    # Test bm_lewis
    print("Generating with bm_lewis...")
    samples, sr = kokoro.create(test_text, voice="bm_lewis", speed=0.92, lang="en-gb")
    wav_path = os.path.join(out_dir, "kokoro_lewis.wav")
    save_wav(wav_path, samples, sr)
    mp3_path = os.path.join(out_dir, "kokoro_lewis.mp3")
    subprocess.run(["ffmpeg", "-i", wav_path, "-codec:a", "libmp3lame", "-qscale:a", "2", mp3_path, "-y"], capture_output=True)
    print(f"✓ Saved {mp3_path} ({os.path.getsize(mp3_path) / 1024:.1f} KB)")

if __name__ == "__main__":
    test()
