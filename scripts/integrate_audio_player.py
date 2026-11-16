import re
from bs4 import BeautifulSoup

file_path = r"c:\Users\aishw\Downloads\CBSE Eng\HTML\going_places_cbse_mastery.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 1. Update Passage Cards with Audio Buttons
for p in soup.find_all("article", class_="passage-card"):
    pid = p.get("id") # passage-1
    num_match = re.search(r"\d+", pid)
    num = int(num_match.group(0)) if num_match else 1
    
    meta = p.find("div", class_="passage-meta")
    if meta:
        # Check if button already exists
        if not meta.find("button", class_="audio-btn"):
            span_right = meta.find("span", string=re.compile(r"SECTION // STUDY MANUAL"))
            
            # Wrap right side
            meta_right = soup.new_tag("div", attrs={"class": "passage-meta-right"})
            
            btn = soup.new_tag("button", attrs={
                "class": "audio-btn",
                "data-passage": str(num),
                "data-src": f"../audio/going_places/passage_{num:02d}.mp3",
                "aria-label": f"Listen to Passage {num}",
                "title": f"Listen to Passage {num}"
            })
            btn.string = "[ ▶ LISTEN ]"
            
            meta_right.append(btn)
            if span_right:
                span_right.extract()
                meta_right.append(span_right)
            meta.append(meta_right)

# 2. Add Audio Dock before </body> if not present
if not soup.find("div", id="audio-dock"):
    dock_html = """
<div class="audio-dock" id="audio-dock" role="region" aria-label="Audio Narration Player">
  <div class="dock-header-row">
    <div class="dock-title-group">
      <span class="dock-badge">AUDIO</span>
      <span class="dock-title" id="dock-title">Passage 1</span>
    </div>
    <div class="dock-time" id="dock-time">0:00 / 0:00</div>
    <button class="dock-close-btn" id="dock-close" title="Close Audio Player" aria-label="Close">✕</button>
  </div>
  <div class="dock-controls-row">
    <div class="dock-ctrl-btns">
      <button class="dock-ctrl-btn" id="dock-prev" title="Previous Passage" aria-label="Previous">⏮</button>
      <button class="dock-ctrl-btn dock-btn-play" id="dock-play" title="Play/Pause" aria-label="Play">[ ❚❚ PAUSE ]</button>
      <button class="dock-ctrl-btn" id="dock-next" title="Next Passage" aria-label="Next">⏭</button>
    </div>
    <div class="dock-progress-wrap">
      <input type="range" class="dock-seeker" id="dock-seeker" value="0" min="0" max="100" step="0.1" aria-label="Audio scrubber">
    </div>
    <div class="dock-speed-group">
      <button class="dock-speed-btn active" data-speed="1.0" aria-label="Normal speed">1.0x</button>
      <button class="dock-speed-btn" data-speed="1.25" aria-label="1.25x speed">1.25x</button>
      <button class="dock-speed-btn" data-speed="1.5" aria-label="1.5x speed">1.5x</button>
    </div>
  </div>
</div>
"""
    dock_soup = BeautifulSoup(dock_html, "html.parser")
    soup.body.append(dock_soup.find("div", id="audio-dock"))

# 3. Add CSS for Audio Player
audio_css = """
/* Audio Player & Dock System */
.passage-meta-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.audio-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  color: var(--text-color);
  border: 1px solid var(--border-color);
  padding: 3px 9px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  cursor: pointer;
  transition: all 0.15s ease;
  border-radius: 2px;
  user-select: none;
}

.audio-btn:hover {
  background: var(--text-color);
  color: var(--bg-color);
  border-color: var(--text-color);
}

.audio-btn.playing {
  background: var(--text-color);
  color: var(--bg-color);
  border-color: var(--text-color);
}

.passage-card.audio-active {
  border-left: 3px solid var(--text-color);
}

.audio-dock {
  position: fixed;
  bottom: 1.5rem;
  left: 2rem;
  max-width: 660px;
  width: calc(100% - 15rem);
  background: var(--bg-color);
  color: var(--text-color);
  border: 2px solid var(--text-color);
  padding: 10px 16px;
  font-family: var(--font-mono);
  font-size: 0.78rem;
  z-index: 990;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  display: none;
  flex-direction: column;
  gap: 8px;
  border-radius: 2px;
}

[data-theme="dark"] .audio-dock {
  box-shadow: 0 8px 24px rgba(0,0,0,0.6);
}

.audio-dock.active {
  display: flex;
  animation: dockSlideUp 0.2s ease-out;
}

@keyframes dockSlideUp {
  from { transform: translateY(16px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.dock-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.dock-title-group {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.dock-badge {
  background: var(--text-color);
  color: var(--bg-color);
  padding: 1px 6px;
  font-size: 0.68rem;
  border-radius: 2px;
  flex-shrink: 0;
}

.dock-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dock-time {
  font-size: 0.72rem;
  color: var(--text-muted);
  flex-shrink: 0;
}

.dock-controls-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.dock-ctrl-btns {
  display: flex;
  align-items: center;
  gap: 6px;
}

.dock-ctrl-btn {
  background: transparent;
  color: var(--text-color);
  border: 1px solid var(--border-color);
  padding: 3px 8px;
  font-family: var(--font-mono);
  font-size: 0.72rem;
  font-weight: 700;
  cursor: pointer;
  border-radius: 2px;
  transition: all 0.15s ease;
}

.dock-ctrl-btn:hover {
  background: var(--text-color);
  color: var(--bg-color);
  border-color: var(--text-color);
}

.dock-speed-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.dock-speed-btn {
  background: transparent;
  color: var(--text-muted);
  border: none;
  padding: 2px 4px;
  font-family: var(--font-mono);
  font-size: 0.70rem;
  cursor: pointer;
}

.dock-speed-btn.active {
  color: var(--text-color);
  font-weight: 700;
  text-decoration: underline;
}

.dock-progress-wrap {
  flex: 1;
  display: flex;
  align-items: center;
}

.dock-seeker {
  width: 100%;
  height: 4px;
  background: var(--border-color);
  appearance: none;
  cursor: pointer;
  border-radius: 2px;
  outline: none;
}

.dock-seeker::-webkit-slider-thumb {
  appearance: none;
  width: 12px;
  height: 12px;
  background: var(--text-color);
  cursor: pointer;
  border-radius: 50%;
}

.dock-close-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 1rem;
  cursor: pointer;
  padding: 0 4px;
  line-height: 1;
}

.dock-close-btn:hover {
  color: var(--text-color);
}

@media (max-width: 900px) {
  .audio-dock {
    left: 1rem;
    right: 1rem;
    bottom: 4.5rem;
    width: auto;
    max-width: none;
  }
}
"""

style_tag = soup.find("style")
if "/* Audio Player & Dock System */" not in style_tag.string:
    style_tag.string = style_tag.string + "\n" + audio_css

# 4. Add Audio Player Script
audio_script = """
/* Minimalist Audio Player Controller */
(function() {
  const audio = new Audio();
  let currentPassage = null;
  let isSeeking = false;
  let currentSpeed = 1.0;

  const dock = document.getElementById('audio-dock');
  const dockTitle = document.getElementById('dock-title');
  const dockTime = document.getElementById('dock-time');
  const dockPlay = document.getElementById('dock-play');
  const dockPrev = document.getElementById('dock-prev');
  const dockNext = document.getElementById('dock-next');
  const dockSeeker = document.getElementById('dock-seeker');
  const dockClose = document.getElementById('dock-close');
  const speedBtns = document.querySelectorAll('.dock-speed-btn');
  const audioBtns = document.querySelectorAll('.audio-btn');

  function formatTime(sec) {
    if (isNaN(sec) || !isFinite(sec)) return "0:00";
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return m + ":" + (s < 10 ? "0" : "") + s;
  }

  function getPassageBtn(num) {
    return document.querySelector('.audio-btn[data-passage="' + num + '"]');
  }

  function getPassageHeadline(num) {
    const card = document.getElementById('passage-' + num);
    if (!card) return 'Passage ' + num;
    const hl = card.querySelector('.passage-headline');
    return hl ? hl.textContent.trim() : 'Passage ' + num;
  }

  function setPlayingState(num, isPlaying) {
    audioBtns.forEach(b => {
      b.textContent = '[ ▶ LISTEN ]';
      b.classList.remove('playing');
    });
    document.querySelectorAll('.passage-card').forEach(c => c.classList.remove('audio-active'));

    if (num) {
      const btn = getPassageBtn(num);
      const card = document.getElementById('passage-' + num);
      if (btn && isPlaying) {
        btn.textContent = '[ ❚❚ PAUSE ]';
        btn.classList.add('playing');
      }
      if (card && isPlaying) {
        card.classList.add('audio-active');
      }
    }

    if (dockPlay) {
      dockPlay.textContent = isPlaying ? '[ ❚❚ PAUSE ]' : '[ ▶ PLAY ]';
    }
  }

  function playPassage(num) {
    const btn = getPassageBtn(num);
    if (!btn) return;

    if (currentPassage === num) {
      if (audio.paused) {
        audio.play();
        setPlayingState(num, true);
      } else {
        audio.pause();
        setPlayingState(num, false);
      }
      return;
    }

    currentPassage = num;
    const src = btn.getAttribute('data-src');
    audio.src = src;
    audio.playbackRate = currentSpeed;
    audio.play().catch(e => console.warn('Audio play error:', e));

    dockTitle.textContent = getPassageHeadline(num);
    dock.classList.add('active');
    setPlayingState(num, true);
  }

  audioBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      const num = parseInt(this.getAttribute('data-passage'), 10);
      playPassage(num);
    });
  });

  if (dockPlay) {
    dockPlay.addEventListener('click', function() {
      if (!currentPassage) return;
      if (audio.paused) {
        audio.play();
        setPlayingState(currentPassage, true);
      } else {
        audio.pause();
        setPlayingState(currentPassage, false);
      }
    });
  }

  if (dockPrev) {
    dockPrev.addEventListener('click', function() {
      if (!currentPassage) return;
      if (currentPassage > 1) {
        playPassage(currentPassage - 1);
      }
    });
  }

  if (dockNext) {
    dockNext.addEventListener('click', function() {
      if (!currentPassage) return;
      if (currentPassage < audioBtns.length) {
        playPassage(currentPassage + 1);
      }
    });
  }

  audio.addEventListener('timeupdate', function() {
    if (!isSeeking && audio.duration) {
      dockSeeker.value = (audio.currentTime / audio.duration) * 100;
      dockTime.textContent = formatTime(audio.currentTime) + ' / ' + formatTime(audio.duration);
    }
  });

  audio.addEventListener('loadedmetadata', function() {
    dockTime.textContent = formatTime(audio.currentTime) + ' / ' + formatTime(audio.duration);
  });

  audio.addEventListener('ended', function() {
    setPlayingState(currentPassage, false);
    if (currentPassage < audioBtns.length) {
      playPassage(currentPassage + 1);
    }
  });

  if (dockSeeker) {
    dockSeeker.addEventListener('input', function() {
      isSeeking = true;
    });
    dockSeeker.addEventListener('change', function() {
      if (audio.duration) {
        audio.currentTime = (dockSeeker.value / 100) * audio.duration;
      }
      isSeeking = false;
    });
  }

  speedBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      speedBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      currentSpeed = parseFloat(this.getAttribute('data-speed'));
      audio.playbackRate = currentSpeed;
    });
  });

  if (dockClose) {
    dockClose.addEventListener('click', function() {
      audio.pause();
      setPlayingState(currentPassage, false);
      dock.classList.remove('active');
    });
  }
})();
"""

script_tag = soup.new_tag("script")
script_tag.string = audio_script
soup.body.append(script_tag)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("Successfully integrated audio player into going_places_cbse_mastery.html!")
