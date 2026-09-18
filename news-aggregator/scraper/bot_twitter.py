import feedparser
import re
import requests
import hashlib  # Bir xil ID chiqaruvchi barqaror shifrlash
from bs4 import BeautifulSoup
from save_to_firebase import save_news_item

TWITTER_RSS_FEEDS = [
    {
        "source_name": "X / AI & Tech Trends",
        "category": "ai",
        "cat_name": "Sun'iy Intellekt (AI)",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/"
    },
    {
        "source_name": "X / Crypto Alerts",
        "category": "crypto",
        "cat_name": "Kripto & Web3",
        "url": "https://cointelegraph.com/rss"
    },
    {
        "source_name": "X / Startups & VC",
        "category": "startup",
        "cat_name": "Startap & Biznes",
        "url": "https://techcrunch.com/category/startups/feed/"
    },
    {
        "source_name": "X / Gaming News",
        "category": "gaming",
        "cat_name": "Gaming & O'yinlar",
        "url": "https://kotaku.com/rss"
    }
]

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', raw_html).strip()

def fetch_real_article_image(article_url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        res = requests.get(article_url, headers=headers, timeout=6)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            og_img = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "twitter:image"})
            if og_img and og_img.get("content"):
                return og_img["content"]
    except Exception:
        pass
    return ""

def scrape_twitter_feeds():
    print("--- TWITTER SCRAPER (DUBLIKATSIZ) BOSHLANDI ---")
    
    for feed_info in TWITTER_RSS_FEEDS:
        print(f"[*] O'qilmoqda: {feed_info['source_name']}")
        try:
            feed = feedparser.parse(feed_info["url"])
            
            for entry in feed.entries[:4]:
                title = entry.title
                link = entry.link
                
                # ENG ASOSIY JOYI: MD5 linkni doim bir xil qat'iy ID ga aylantiradi
                unique_hash = hashlib.md5(link.encode('utf-8')).hexdigest()[:16]
                unique_id = f"feed_{unique_hash}"

                full_text = clean_html(entry.get("summary", entry.get("description", "")))
                summary = full_text[:160] + "..."

                image_url = ""
                if hasattr(entry, 'enclosures') and len(entry.enclosures) > 0:
                    image_url = entry.enclosures[0].get('href', '')

                if not image_url and "media_content" in entry and len(entry.media_content) > 0:
                    image_url = entry.media_content[0].get("url", "")
                
                if not image_url and link:
                    image_url = fetch_real_article_image(link)

                if not image_url:
                    image_url = f"https://picsum.photos/seed/{unique_id}/800/500"

                news_item = {
                    "id": unique_id,
                    "title": title,
                    "summary": summary,
                    "fullText": full_text if len(full_text) > 30 else title,
                    "imageUrl": image_url,
                    "category": feed_info["category"],
                    "categoryName": feed_info["cat_name"],
                    "source": feed_info["source_name"],
                    "sourceUrl": link
                }

                save_news_item(news_item)

        except Exception as e:
            print(f"[!] Xatolik: {e}")

    print("--- YAKUNLANDI ---")

if __name__ == "__main__":
    scrape_twitter_feeds()