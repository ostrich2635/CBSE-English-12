import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# \U0001F399\ufe0f F5-TTS Voice Cloning: Derek Perkins — CBSE Class 12 'Going Places'\n",
    "\n",
    "This notebook uses **F5-TTS (Flow-matching Diffusion Transformer)** on a free Google Colab GPU to clone the voice of **Derek Perkins** and synthesize all 16 passages of CBSE Class 12 English Chapter 8 (*Going Places*).\n",
    "\n",
    "### \u26a1 1-Click Instructions (~3 to 4 minutes total):\n",
    "1. **Enable Free GPU:** Go to **Runtime \u2192 Change runtime type \u2192 T4 GPU \u2192 Save**.\n",
    "2. **Run All:** Click **Runtime \u2192 Run all** (`Ctrl + F9`).\n",
    "3. The reference audio and all 16 passages load automatically from the repository.\n",
    "4. When finished, it automatically compresses and downloads `going_places_audio.zip`!\n",
    "5. Extract the `.mp3` files into your local project folder: `CBSE Eng/audio/going_places/`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 1: Install F5-TTS and dependencies\n",
    "!pip install --quiet git+https://github.com/SWivid/F5-TTS.git\n",
    "!pip install --quiet pydub soundfile torchaudio"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 2: Download Reference Audio of Derek Perkins\n",
    "import os\n",
    "\n",
    "ref_text = \"In the previous chapter we saw that although Sapiens had already populated East Africa 150,000 years ago, they began to overrun the rest of planet Earth and drive other human species to extinction only about 70,000 years ago.\"\n",
    "ref_file = \"derek_perkins_ref.wav\"\n",
    "\n",
    "if not os.path.exists(ref_file):\n",
    "    print(\"Downloading Derek Perkins reference sample from GitHub...\")\n",
    "    !curl -s -L -o derek_perkins_ref.wav https://raw.githubusercontent.com/ostrich2635/CBSE-English-12/main/audio/derek_perkins_ref.wav\n",
    "\n",
    "assert os.path.exists(ref_file) and os.path.getsize(ref_file) > 1000, \"Reference audio failed to download!\"\n",
    "print(f\"\u2713 Reference audio ready: {ref_file} ({os.path.getsize(ref_file)/1024:.1f} KB)\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 3: Load Going Places 16 Passages\n",
    "import json\n",
    "\n",
    "passages_data = \"\"\"__PASSAGES_JSON__\"\"\"\n",
    "passages = json.loads(passages_data)\n",
    "print(f\"\u2713 Loaded {len(passages)} passages for Going Places.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 4: Batch Inference using F5-TTS\n",
    "import subprocess\n",
    "from f5_tts.api import F5TTS\n",
    "\n",
    "os.makedirs(\"going_places_audio\", exist_ok=True)\n",
    "f5tts = F5TTS()\n",
    "\n",
    "for p in passages:\n",
    "    base_name = os.path.splitext(p[\"filename\"])[0]\n",
    "    wav_out = os.path.join(\"going_places_audio\", f\"{base_name}.wav\")\n",
    "    mp3_out = os.path.join(\"going_places_audio\", f\"{base_name}.mp3\")\n",
    "    speech_text = f\"{p['title']}. {p['text']}\"\n",
    "    \n",
    "    print(f\"Generating {p['id']} ({len(speech_text.split())} words): {p['title']}...\")\n",
    "    f5tts.infer(\n",
    "        ref_file=ref_file,\n",
    "        ref_text=ref_text,\n",
    "        gen_text=speech_text,\n",
    "        file_wave=wav_out\n",
    "    )\n",
    "    \n",
    "    # Convert to web-optimized MP3\n",
    "    subprocess.run([\"ffmpeg\", \"-y\", \"-i\", wav_out, \"-codec:a\", \"libmp3lame\", \"-qscale:a\", \"2\", mp3_out], capture_output=True)\n",
    "    if os.path.exists(wav_out):\n",
    "        os.remove(wav_out)\n",
    "    \n",
    "    print(f\"  \u2713 Finished {mp3_out} ({os.path.getsize(mp3_out)/1024:.1f} KB)\")\n",
    "\n",
    "print(\"\\n\u2728 All 16 passages generated with Derek Perkins' voice clone!\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 5: Compress and Download to PC\n",
    "!zip -j -r going_places_audio.zip going_places_audio/\n",
    "from google.colab import files\n",
    "files.download(\"going_places_audio.zip\")\n",
    "print(\"\u2705 Download initiated! Once downloaded, unzip the 16 .mp3 files into CBSE Eng/audio/going_places/ to replace the preview audios.\")"
   ]
  }
 ],
 "metadata": {
  "accelerator": "GPU",
  "colab": {
   "provenance": []
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}

# Read passages
with open(r"c:\Users\aishw\Downloads\CBSE Eng\audio\going_places_passages.json", "r", encoding="utf-8") as f:
    passages_json = f.read()

cell_3_src = notebook_content["cells"][3]["source"]
for i in range(len(cell_3_src)):
    if "__PASSAGES_JSON__" in cell_3_src[i]:
        cell_3_src[i] = cell_3_src[i].replace("__PASSAGES_JSON__", passages_json)

out_nb = r"c:\Users\aishw\Downloads\CBSE Eng\notebooks\Derek_Perkins_Voice_Clone_Going_Places.ipynb"
with open(out_nb, "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=1)

print(f"Updated Colab notebook at {out_nb}")
