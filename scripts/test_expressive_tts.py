import asyncio
import edge_tts
import os

test_text = """
“When I leave,” Sophie said, coming home from school, “I’m going to have a boutique.”

Jansie, linking arms with her along the street; looked doubtful.

“Takes money, Soaf, something like that.”

“I’ll find it,” Sophie said, staring far down the street.
"""

# Let's test a few variations:
# 1. Ryan with warm baritone pitch and contemplative pacing (-8% rate, -3Hz pitch)
# 2. BrianNeural (often rated as one of the most natural, human-sounding male narrators)
# 3. ChristopherNeural (expressive storytelling voice)
# 4. SSML with dramatic dialogue breaks

ssml_text = """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-GB">
<voice name="en-GB-RyanNeural">
<prosody rate="-8%" pitch="-2Hz">
<p>
<s><prosody pitch="+1Hz">“When I leave,”</prosody> Sophie said, coming home from school, <prosody pitch="+1Hz">“I’m going to have a boutique.”</prosody></s>
<break time="450ms"/>
<s>Jansie, linking arms with her along the street, looked doubtful.</s>
<break time="400ms"/>
<s><prosody pitch="-1Hz">“Takes money, Soaf, something like that.”</prosody></s>
<break time="450ms"/>
<s><prosody pitch="+1Hz">“I’ll find it,”</prosody> Sophie said, staring far down the street.</s>
</p>
</prosody>
</voice>
</speak>"""

async def test():
    out_dir = r"c:\Users\aishw\Downloads\CBSE Eng\audio\test_tones"
    os.makedirs(out_dir, exist_ok=True)
    
    # Test 1: Ryan with deeper pitch and slower cadence
    comm1 = edge_tts.Communicate(test_text, "en-GB-RyanNeural", rate="-10%", pitch="-3Hz")
    await comm1.save(os.path.join(out_dir, "ryan_deep.mp3"))
    print("Saved ryan_deep.mp3")

    # Test 2: Brian (extremely natural human narrator)
    comm2 = edge_tts.Communicate(test_text, "en-US-BrianNeural", rate="-6%", pitch="-1Hz")
    await comm2.save(os.path.join(out_dir, "brian_warm.mp3"))
    print("Saved brian_warm.mp3")

    # Test 3: SSML with expressive punctuation and prosody
    # Note: edge_tts communicate doesn't take raw SSML string directly in Communicate(text),
    # but we can format text with punctuation or custom pauses.

asyncio.run(test())
