from bot_telegram import run_all_telegram
from bot_twitter import scrape_twitter_feeds

def main():
    print("--- BULUTLI SCRAPER ISHGA TUSHDI ---")
    try:
        run_all_telegram()
    except Exception as e:
        print(f"Telegramda xatolik: {e}")

    try:
        scrape_twitter_feeds()
    except Exception as e:
        print(f"Twitterda xatolik: {e}")

    print("--- HAMMASI BAZAGA YOZILDI VA YAKUNLANDI ---")

if __name__ == "__main__":
    main()