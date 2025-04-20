from TikTokApi import TikTokApi
import asyncio
import yt_dlp
import os

# البحث حسب هاشتاغ
async def fetch_hashtag_videos(tag="شرطة", count=10):
    async with TikTokApi() as api:
        videos = await api.hashtag(name=tag).videos(count=count)

        os.makedirs("downloads/tiktok", exist_ok=True)
        for idx, video in enumerate(videos):
            url = video.as_dict['video']['downloadAddr']
            output_path = f"downloads/tiktok/tiktok_{idx}.mp4"
            ydl_opts = {"outtmpl": output_path}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"تم تحميل: {output_path}")

asyncio.run(fetch_hashtag_videos("شرطة"))
