import os
import firebase_admin
from firebase_admin import credentials, firestore

# serviceAccountKey.json faylini shu papkadan topish
current_dir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(current_dir, "serviceAccountKey.json")

# Firebase'ni ishga tushiramiz
if not os.path.exists(cred_path):
    print(f"DIQQAT: {cred_path} fayli topilmadi! Firebase kalitini scraper papkasiga tashlang.")
else:
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

db = firestore.client() if firebase_admin._apps else None

def save_news_item(news_item):
    """
    Yangilikni bazaga yozuvchi funksiya.
    Bir xil yangilik ikki marta yozilmaydi (Dublikatdan himoya).
    """
    if not db:
        print("[!] Xatolik: Firebase bazasi ulanmagan.")
        return False

    try:
        # Har bir yangilikka berilgan unikal ID bo'yicha bazadan tekshiramiz
        doc_id = str(news_item["id"])
        doc_ref = db.collection("news").document(doc_id)
        
        # Agar bu yangilik bazada allaqachon bo'lsa, qayta yozmaymiz
        if doc_ref.get().exists:
            print(f"[-] Allaqachon bor: {news_item['title'][:35]}...")
            return False

        # Yangi bo'lsa, Firebase server vaqti bilan bazaga saqlaymiz
        data_to_save = {
            "title": news_item.get("title", "Sarlavhasiz"),
            "summary": news_item.get("summary", ""),
            "fullText": news_item.get("fullText", ""),
            "imageUrl": news_item.get("imageUrl", ""),
            "category": news_item.get("category", "it"),
            "categoryName": news_item.get("categoryName", "IT & Texno"),
            "source": news_item.get("source", "Internet"),
            "sourceUrl": news_item.get("sourceUrl", "#"),
            "createdAt": firestore.SERVER_TIMESTAMP
        }

        doc_ref.set(data_to_save)
        print(f"[+] YANGI QO'SHILDI: {news_item['title'][:40]}...")
        return True

    except Exception as e:
        print(f"[!] Bazaga yozishda xatolik: {e}")
        return False