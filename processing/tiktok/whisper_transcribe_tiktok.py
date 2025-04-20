import os
import whisper

model = whisper.load_model("base")

input_dir = "downloads/tiktok"
output_dir = "processing/tiktok"
os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(input_dir):
    if file.endswith(".mp4"):
        audio_path = os.path.join(input_dir, file)
        print(f"تحويل: {audio_path}")
        result = model.transcribe(audio_path)
        text = result['text']
        with open(os.path.join(output_dir, f"{file}.txt"), "w", encoding='utf-8') as out_file:
            out_file.write(text)
