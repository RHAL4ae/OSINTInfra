import os
import whisper
import urllib.request

# تحميل موديل Whisper
model = whisper.load_model("base")

# تحميل الفيديوهات من الروابط
with open("downloads/snap_urls.txt", "r") as f:
    urls = f.readlines()

for idx, url in enumerate(urls):
    url = url.strip()
    local_path = f"downloads/snap_{idx}.mp4"
    try:
        urllib.request.urlretrieve(url, local_path)
        print(f"تم تحميل: {local_path}")
    except:
        print(f"فشل تحميل: {url}")

# تحويل الصوت إلى نص
results = []
for file in os.listdir("downloads"):
    if file.endswith(".mp4"):
        audio_path = os.path.join("downloads", file)
        print(f"تحويل: {audio_path}")
        result = model.transcribe(audio_path)
        text = result['text']
        with open(f"processing/{file}.txt", "w", encoding='utf-8') as out_file:
            out_file.write(text)
