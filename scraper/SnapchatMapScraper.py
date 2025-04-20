from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

# إعداد المتصفح
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# موقع الخريطة (عجمان كمثال)
location_url = "https://map.snapchat.com/@25.4052,55.5136,14.5z"
driver.get(location_url)
time.sleep(10)

# جمع روابط الفيديوهات
snaps = driver.find_elements("css selector", "video")
snap_urls = [snap.get_attribute("src") for snap in snaps if snap.get_attribute("src")]

# حفظ الروابط في ملف نصي
os.makedirs("downloads", exist_ok=True)
with open("downloads/snap_urls.txt", "w") as f:
    for url in snap_urls:
        f.write(url + "\n")

driver.quit()
print("تم جمع الروابط بنجاح.")
