import asyncio
import edge_tts
import json
import os

json_path = r"c:\Users\aishw\Downloads\CBSE Eng\audio\going_places_passages.json"
out_dir = r"c:\Users\aishw\Downloads\CBSE Eng\audio\going_places"
os.makedirs(out_dir, exist_ok=True)

with open(json_path, "r", encoding="utf-8") as f:
    passages = json.load(f)

# Use en-GB-RyanNeural for a rich, refined British narrator cadence
VOICE = "en-GB-RyanNeural"

async def generate_all():
    print(f"Generating audio for {len(passages)} passages using {VOICE}...")
    for p in passages:
        out_file = os.path.join(out_dir, p["filename"])
        print(f"Generating {p['id']} -> {p['filename']} ({len(p['text'].split())} words)...")
        # Prepend title for context in audio
        speech_text = f"{p['title']}. {p['text']}"
        comm = edge_tts.Communicate(speech_text, VOICE, rate="-4%")
        await comm.save(out_file)
        size_kb = os.path.getsize(out_file) / 1024
        print(f"  ✓ Saved {p['filename']} ({size_kb:.1f} KB)")

    print("\nAll 16 passages successfully generated!")

if __name__ == "__main__":
    asyncio.run(generate_all())
