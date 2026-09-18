import re
import requests
from bs4 import BeautifulSoup
from save_to_firebase import save_news_item

TARGET_CHANNELS = [
    {"channel": "openai_news_channel", "category": "ai", "cat_name": "Sun'iy Intellekt (AI)"},
    {"channel": "cointelegraph", "category": "crypto", "cat_name": "Kripto & Web3"},
    {"channel": "tproger_official", "category": "it", "cat_name": "IT & Dasturlash"},
    {"channel": "vcnews", "category": "startup", "cat_name": "Startap & Biznes"},
    {"channel": "thehackernews", "category": "security", "cat_name": "Kiberxavfsizlik"},
    {"channel": "wylsacomred", "category": "gadgets", "cat_name": "Gadjetlar"},
    {"channel": "popmech", "category": "science", "cat_name": "Fan & Kosmos"},
    {"channel": "igromania", "category": "gaming", "cat_name": "Gaming & O'yinlar"},
    {"channel": "uxlive", "category": "design", "cat_name": "Dizayn & 3D"},
    {"channel": "autonews_ru", "category": "auto", "cat_name": "Avto & Texno"}
]

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_image(msg, unique_id):
    """Rasmni barcha joylardan chuqur qidirish"""
    image_url = ""

    # 1. Postning to'g'ridan-to'g'ri fotosi
    photo = msg.find("a", class_="tgme_widget_message_photo_wrap")
    if photo and "style" in photo.attrs:
        match = re.search(r"url\(['\"]?(.*?)['\"]?\)", photo["style"])
        if match:
            return match.group(1)

    # 2. Havola preview rasmi (Link preview image)
    link_preview = msg.find("i", class_="link_preview_image") or msg.find("i", class_="link_preview_right_image")
    if link_preview and "style" in link_preview.attrs:
        match = re.search(r"url\(['\"]?(.*?)['\"]?\)", link_preview["style"])
        if match:
            return match.group(1)

    # 3. Video preview thumb
    video_thumb = msg.find("i", class_="tgme_widget_message_video_thumb")
    if video_thumb and "style" in video_thumb.attrs:
        match = re.search(r"url\(['\"]?(.*?)['\"]?\)", video_thumb["style"])
        if match:
            return match.group(1)

    # 4. Agar postda rasm mutlaqo bo'lmasa - har bir xabar uchun BETAKROR tasodifiy rasm
    return f"https://picsum.photos/seed/{unique_id}/800/500"

def scrape_channel(channel_info):
    username = channel_info["channel"]
    category = channel_info["category"]
    cat_name = channel_info["cat_name"]

    url = f"https://t.me/s/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.text, "html.parser")
        messages = soup.find_all("div", class_="tgme_widget_message")

        for msg in messages[-4:]:
            post_id_raw = msg.get("data-post")
            if not post_id_raw:
                continue

            unique_id = f"tg_{post_id_raw.replace('/', '_')}"
            source_url = f"https://t.me/{post_id_raw}"

            text_block = msg.find("div", class_="tgme_widget_message_text")
            if not text_block:
                continue

            full_text = text_block.get_text(separator="\n").strip()
            if len(full_text) < 20:
                continue

            lines = [l.strip() for l in full_text.split("\n") if l.strip()]
            title = lines[0] if lines else "Yangi xabar"
            if len(title) > 90:
                title = title[:90] + "..."

            summary = clean_text(full_text)[:160] + "..."
            image_url = extract_image(msg, unique_id)

            news_item = {
                "id": unique_id,
                "title": title,
                "summary": summary,
                "fullText": full_text,
                "imageUrl": image_url,
                "category": category,
                "categoryName": cat_name,
                "source": f"Telegram (@{username})",
                "sourceUrl": source_url
            }

            save_news_item(news_item)

    except Exception as e:
        print(f"[!] {username} xatolik: {e}")

def run_all_telegram():
    print("--- KUCHAYTIRILGAN TELEGRAM SCRAPER ISHGA TUSHDI ---")
    for ch in TARGET_CHANNELS:
        scrape_channel(ch)
    print("--- YAKUNLANDI ---")

if __name__ == "__main__":
    run_all_telegram()