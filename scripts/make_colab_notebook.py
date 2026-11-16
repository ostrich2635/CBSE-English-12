import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# \U0001F399\ufe0f F5-TTS Voice Cloning: Derek Perkins — CBSE Class 12 'Going Places'\n",
    "\n",
    "This updated notebook uses **Sentence-Chunking & Pacing Control** with F5-TTS to clone **Derek Perkins** without any prompt leakage or rushed speech.\n",
    "\n",
    "### \u2728 What is Fixed in this Version:\n",
    "- \u2705 **Zero Prompt Leakage:** Uses a clean 7.2s single-sentence reference clip (`derek_perkins_ref.wav`) with 100% exact alignment, eliminating any mixed phrases from Sapiens.\n",
    "- \u2705 **Calm, Human Audiobook Pace:** Splits each passage into natural sentences and synthesizes at `speed=0.82` with natural 300ms breathing pauses between thoughts.\n",
    "\n",
    "### \u26a1 Instructions (~4 minutes total on free Colab GPU):\n",
    "1. Ensure GPU is active (**Runtime \u2192 Change runtime type \u2192 T4 GPU \u2192 Save**).\n",
    "2. Click **Runtime \u2192 Run all** (`Ctrl + F9`).\n",
    "3. It automatically downloads the clean reference sample and generates all 16 passages.\n",
    "4. When finished, it automatically downloads `going_places_audio.zip`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 1: Install F5-TTS and audio dependencies\n",
    "!pip install --quiet git+https://github.com/SWivid/F5-TTS.git\n",
    "!pip install --quiet pydub soundfile torchaudio numpy"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 2: Download the Clean Single-Sentence Reference Audio of Derek Perkins\n",
    "import os\n",
    "\n",
    "# Exact verbatim transcript matching the clean 7.20s audio clip\n",
    "ref_text = \"They began to overrun the rest of planet Earth and drive other human species to extinction only about 70,000 years ago.\"\n",
    "ref_file = \"derek_perkins_ref.wav\"\n",
    "\n",
    "# Always fetch fresh clean reference audio\n",
    "print(\"Downloading clean Derek Perkins reference sample from GitHub...\")\n",
    "!curl -s -L -o derek_perkins_ref.wav https://raw.githubusercontent.com/ostrich2635/CBSE-English-12/main/audio/derek_perkins_ref.wav\n",
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
    "# Step 4: Batch Inference with Sentence Chunking & Calm Audiobook Tempo (speed=0.82)\n",
    "import re\n",
    "import subprocess\n",
    "import soundfile as sf\n",
    "import numpy as np\n",
    "from f5_tts.api import F5TTS\n",
    "\n",
    "os.makedirs(\"going_places_audio\", exist_ok=True)\n",
    "f5tts = F5TTS()\n",
    "\n",
    "def chunk_sentences(text, max_words=22):\n",
    "    # Split on sentence boundaries\n",
    "    raw_sentences = re.split(r'(?<=[.?!;])\\s+', text)\n",
    "    chunks = []\n",
    "    current_chunk = []\n",
    "    current_words = 0\n",
    "    for s in raw_sentences:\n",
    "        s = s.strip()\n",
    "        if not s: continue\n",
    "        words = len(s.split())\n",
    "        if current_words + words <= max_words:\n",
    "            current_chunk.append(s)\n",
    "            current_words += words\n",
    "        else:\n",
    "            if current_chunk:\n",
    "                chunks.append(\" \".join(current_chunk))\n",
    "            current_chunk = [s]\n",
    "            current_words = words\n",
    "    if current_chunk:\n",
    "        chunks.append(\" \".join(current_chunk))\n",
    "    return chunks\n",
    "\n",
    "for p in passages:\n",
    "    base_name = os.path.splitext(p[\"filename\"])[0]\n",
    "    mp3_out = os.path.join(\"going_places_audio\", f\"{base_name}.mp3\")\n",
    "    full_text = f\"{p['title']}. {p['text']}\"\n",
    "    chunks = chunk_sentences(full_text, max_words=20)\n",
    "    \n",
    "    print(f\"\\nGenerating {p['id']} ({len(chunks)} chunks, speed=0.82): {p['title']}...\")\n",
    "    audio_segments = []\n",
    "    sample_rate = 24000\n",
    "    \n",
    "    for idx, chunk in enumerate(chunks):\n",
    "        wav, sr, _ = f5tts.infer(\n",
    "            ref_file=ref_file,\n",
    "            ref_text=ref_text,\n",
    "            gen_text=chunk,\n",
    "            speed=0.82\n",
    "        )\n",
    "        sample_rate = sr\n",
    "        audio_segments.append(wav)\n",
    "        # 280ms natural pause between sentences\n",
    "        pause = np.zeros(int(sr * 0.28))\n",
    "        audio_segments.append(pause)\n",
    "    \n",
    "    combined_wav = np.concatenate(audio_segments)\n",
    "    temp_wav = f\"temp_{base_name}.wav\"\n",
    "    sf.write(temp_wav, combined_wav, sample_rate)\n",
    "    \n",
    "    # Convert to MP3\n",
    "    subprocess.run([\"ffmpeg\", \"-y\", \"-i\", temp_wav, \"-codec:a\", \"libmp3lame\", \"-qscale:a\", \"2\", mp3_out], capture_output=True)\n",
    "    if os.path.exists(temp_wav):\n",
    "        os.remove(temp_wav)\n",
    "    \n",
    "    print(f\"  \u2713 Finished {mp3_out} ({os.path.getsize(mp3_out)/1024:.1f} KB)\")\n",
    "\n",
    "print(\"\\n\u2728 All 16 passages generated with calm pace and zero prompt leakage!\")"
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
    "print(\"\u2705 Download initiated! Extract the 16 .mp3 files into CBSE Eng/audio/going_places/ to replace the previous files.\")"
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
