import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# \U0001F399\ufe0f F5-TTS Voice Cloning: Derek Perkins — CBSE Class 12 'Going Places'\n",
    "\n",
    "This notebook clones the voice of **Derek Perkins** (from the Sapiens reference sample) and batch-synthesizes all 16 passages of CBSE Class 12 English Chapter 8 (*Going Places*).\n",
    "\n",
    "### \u26a1 Instructions (Takes ~3 minutes):\n",
    "1. **Enable Free GPU:** Go to **Runtime \u2192 Change runtime type \u2192 T4 GPU \u2192 Save**.\n",
    "2. **Run All:** Click **Runtime \u2192 Run all** (or press `Ctrl + F9`).\n",
    "3. Upload `derek_perkins_ref.wav` when prompted (or it downloads automatically if available).\n",
    "4. When finished, it will automatically download `going_places_audio.zip` containing all 16 `.mp3` files!\n",
    "5. Extract the `.mp3` files into your project's `audio/going_places/` folder."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 1: Install F5-TTS and audio tools\n",
    "!pip install --quiet git+https://github.com/SWivid/F5-TTS.git\n",
    "!pip install --quiet pydub soundfile"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 2: Upload or prepare Reference Audio\n",
    "import os\n",
    "from google.colab import files\n",
    "\n",
    "ref_text = \"In the previous chapter we saw that although Sapiens had already populated East Africa 150,000 years ago, they began to overrun the rest of planet Earth and drive other human species to extinction only about 70,000 years ago.\"\n",
    "ref_file = \"derek_perkins_ref.wav\"\n",
    "\n",
    "if not os.path.exists(ref_file):\n",
    "    print(\"Please upload derek_perkins_ref.wav from your CBSE Eng/audio folder:\")\n",
    "    uploaded = files.upload()\n",
    "    if uploaded:\n",
    "        ref_file = list(uploaded.keys())[0]\n",
    "\n",
    "print(f\"Using reference audio: {ref_file}\")"
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
    "print(f\"Loaded {len(passages)} passages for Going Places.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 4: Batch Inference using F5-TTS\n",
    "from f5_tts.api import F5TTS\n",
    "\n",
    "os.makedirs(\"going_places_audio\", exist_ok=True)\n",
    "f5tts = F5TTS()\n",
    "\n",
    "for p in passages:\n",
    "    out_path = os.path.join(\"going_places_audio\", p[\"filename\"])\n",
    "    speech_text = f\"{p['title']}. {p['text']}\"\n",
    "    print(f\"Synthesizing {p['id']}: {p['title']}...\")\n",
    "    f5tts.infer(\n",
    "        ref_file=ref_file,\n",
    "        ref_text=ref_text,\n",
    "        gen_text=speech_text,\n",
    "        file_wave=out_path\n",
    "    )\n",
    "    print(f\"  \u2713 Finished {p['filename']}\")\n",
    "\n",
    "print(\"\\nAll 16 passages generated successfully!\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Step 5: Compress and Download\n",
    "!zip -r going_places_audio.zip going_places_audio/\n",
    "from google.colab import files\n",
    "files.download(\"going_places_audio.zip\")\n",
    "print(\"Download started! Extract the files into your local 'audio/going_places/' directory.\")"
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

# Read actual passages
with open(r"c:\Users\aishw\Downloads\CBSE Eng\audio\going_places_passages.json", "r", encoding="utf-8") as f:
    passages_json = f.read()

# Insert passages json string
cell_3_src = notebook_content["cells"][3]["source"]
for i in range(len(cell_3_src)):
    if "__PASSAGES_JSON__" in cell_3_src[i]:
        cell_3_src[i] = cell_3_src[i].replace("__PASSAGES_JSON__", passages_json)

out_nb = r"c:\Users\aishw\Downloads\CBSE Eng\notebooks\Derek_Perkins_Voice_Clone_Going_Places.ipynb"
with open(out_nb, "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=1)

print(f"Colab notebook created at {out_nb}")
