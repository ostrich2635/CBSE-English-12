import os
import urllib.request

model_dir = r"c:\Users\aishw\Downloads\CBSE Eng\audio\kokoro_model"
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, "kokoro-v0_19.onnx")
voices_path = os.path.join(model_dir, "voices.bin")

def download_file(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print(f"File already exists: {path}")
        return
    print(f"Downloading {url} to {path}...")
    urllib.request.urlretrieve(url, path)
    print(f"Downloaded {path} ({os.path.getsize(path) / (1024*1024):.1f} MB)")

try:
    download_file("https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx", model_path)
    download_file("https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.bin", voices_path)
    print("Kokoro files ready!")
except Exception as e:
    print(f"Download failed: {e}")
