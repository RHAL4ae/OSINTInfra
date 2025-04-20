from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# صفحة هاشتاغ (عام)
hashtag = "شرطة"
url = f"https://www.instagram.com/explore/tags/{hashtag}/"
driver.get(url)
time.sleep(10)

# جمع أول 10 منشورات
posts = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/p/"]')
post_links = [p.get_attribute("href") for p in posts[:10]]
print("روابط المنشورات:")
for link in post_links:
    print(link)

driver.quit()
