import json
import re
from bs4 import BeautifulSoup
import os

html_path = r"c:\Users\aishw\Downloads\CBSE Eng\HTML\going_places_cbse_mastery.html"
with open(html_path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

passages = []
for p in soup.find_all("article", class_="passage-card"):
    pid = p.get("id")
    num_match = re.search(r"\d+", pid)
    num = int(num_match.group(0)) if num_match else len(passages) + 1
    headline = p.find("div", class_="passage-headline").get_text(strip=True)
    quote = p.find("div", class_="quote-passage")
    
    # Clone quote so we don't mutate DOM if needed
    quote_copy = BeautifulSoup(str(quote), "html.parser")
    label = quote_copy.find("span", class_="quote-label")
    if label:
        label.decompose()
        
    text = quote_copy.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()
    
    passages.append({
        "id": pid,
        "number": num,
        "title": headline,
        "text": text,
        "filename": f"passage_{num:02d}.mp3"
    })

out_json = r"c:\Users\aishw\Downloads\CBSE Eng\audio\going_places_passages.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(passages, f, indent=2, ensure_ascii=False)

print(f"Extracted {len(passages)} passages into {out_json}")
for item in passages[:3]:
    print(f"{item['id']} ({item['filename']}): {item['title']}")
    print(f"  Preview: {item['text'][:100]}...\n")
