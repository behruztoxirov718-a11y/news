from save_to_firebase import db

def clear_all_news():
    docs = db.collection("news").stream()
    count = 0
    for doc in docs:
        doc.reference.delete()
        count += 1
    print(f"[V] Baza tozalandi! Jami {count} ta eski xabar o'chirildi.")

if __name__ == "__main__":
    clear_all_news()