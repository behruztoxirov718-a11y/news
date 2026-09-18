import time
from datetime import datetime
from bot_telegram import run_all_telegram
from bot_twitter import scrape_twitter_feeds

# Yangilanish oralig'i (daqiqada)
INTERVAL_MINUTES = 15

def run_news_aggregator():
    now_str = datetime.now().strftime("%H:%M:%S")
    print("\n" + "="*55)
    print(f"[{now_str}] AVTOMATIK YANGILIKLAR YIG'ISH BOSHLANDI...")
    print("="*55)

    # 1. Telegram kanallarini skanerlash
    try:
        run_all_telegram()
    except Exception as e:
        print(f"[!] Telegramda xatolik: {e}")

    # 2. Twitter / RSS manbalarini skanerlash
    try:
        scrape_twitter_feeds()
    except Exception as e:
        print(f"[!] Twitterda xatolik: {e}")

    finish_str = datetime.now().strftime("%H:%M:%S")
    print("="*55)
    print(f"[{finish_str}] BARCHA MANBALAR TEKSHIRILDI!")
    print(f"Keyingi avtomatik tekshiruv {INTERVAL_MINUTES} daqiqadan so'ng bo'ladi.")
    print("Dasturni to'xtatish uchun terminalda istalgan payt Ctrl + C ni bosing.")
    print("="*55 + "\n")

if __name__ == "__main__":
    print("[*] Smart News Robot ishga tushirildi! Avtomatik monitoring faol.")
    while True:
        run_news_aggregator()
        # 15 daqiqa (15 * 60 soniya) kutish rejimiga o'tadi
        time.sleep(INTERVAL_MINUTES * 60)