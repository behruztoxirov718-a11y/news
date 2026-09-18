import { db } from "./firebase-config.js";
import { 
  collection, 
  query, 
  orderBy, 
  onSnapshot 
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

// DOM elementlari
const newsGrid = document.getElementById("newsGrid");
const categoryButtons = document.querySelectorAll(".cat-btn");
const newsModal = document.getElementById("newsModal");
const closeModalBtn = document.getElementById("closeModalBtn");

// Modal ichidagi elementlar
const modalImage = document.getElementById("modalImage");
const modalCategory = document.getElementById("modalCategory");
const modalSource = document.getElementById("modalSource");
const modalTime = document.getElementById("modalTime");
const modalTitle = document.getElementById("modalTitle");
const modalContent = document.getElementById("modalContent");
const modalLink = document.getElementById("modalLink");

let allNews = []; // Barcha yangiliklarni xotirada saqlab turish uchun
let activeCategory = "all";

// 1. Firebasedan yangiliklarni real-time (jonli) yuklab olish
function initNewsListener() {
  const newsRef = collection(db, "news");
  // Eng so'nggi chiqqanlarini birinchi ko'rsatish
  const q = query(newsRef, orderBy("createdAt", "desc"));

  onSnapshot(q, (snapshot) => {
    allNews = [];
    snapshot.forEach((doc) => {
      allNews.push({ id: doc.id, ...doc.data() });
    });

    renderNews();
  }, (error) => {
    console.error("Xatolik yuz berdi:", error);
    newsGrid.innerHTML = `<div class="loading-spinner">Yangiliklarni yuklashda xatolik: ${error.message}</div>`;
  });
}

// 2. Yangiliklarni ekranga chiroyli qilib chiqarish
function renderNews() {
  // Tanlangan kategoriya bo'yicha saralash
  const filteredNews = activeCategory === "all" 
    ? allNews 
    : allNews.filter(item => item.category?.toLowerCase() === activeCategory.toLowerCase());

  // Agar yangilik hali bo'lmasa
  if (filteredNews.length === 0) {
    newsGrid.innerHTML = `
      <div class="loading-spinner">
        Hozircha yangiliklar yo'q.<br>
        <span style="font-size: 13px; color: #64748b;">Scraper robotni ishga tushirganimizda yangiliklar bu yerga avtomatik tushadi.</span>
      </div>
    `;
    return;
  }

  newsGrid.innerHTML = "";

  filteredNews.forEach((item) => {
    const card = document.createElement("article");
    card.className = "news-card";

    // Sana formatlash
    const timeFormatted = item.createdAt ? new Date(item.createdAt.toDate ? item.createdAt.toDate() : item.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : "Yangi";

    card.innerHTML = `
      <div class="card-img-wrap">
        <img class="card-img" src="${item.imageUrl || 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=600'}" alt="${item.title}" loading="lazy">
        <span class="card-badge">${item.categoryName || item.category || 'Yangilik'}</span>
      </div>
      <div class="card-content">
        <div class="card-meta">
          <span>${item.source || 'Tarmoq'}</span> • <span>${timeFormatted}</span>
        </div>
        <h3 class="card-title">${item.title}</h3>
        <p class="card-summary">${item.summary || item.fullText || ''}</p>
        <div class="card-footer">
          Batafsil o'qish <span>&rarr;</span>
        </div>
      </div>
    `;

    // Ustiga bosganda to'liq oynani (Modal) ochish
    card.addEventListener("click", () => openModal(item, timeFormatted));

    newsGrid.appendChild(card);
  });
}

// 3. Modalni ochish ("Batafsil / Поподробнее")
function openModal(item, timeFormatted) {
  modalImage.src = item.imageUrl || 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?q=80&w=600';
  modalCategory.textContent = item.categoryName || item.category || 'Umumiy';
  modalSource.textContent = item.source || 'Manba';
  modalTime.textContent = timeFormatted;
  modalTitle.textContent = item.title;
  modalContent.textContent = item.fullText || item.summary || 'To\'liq matn mavjud emas.';
  
  if (item.sourceUrl) {
    modalLink.href = item.sourceUrl;
    modalLink.style.display = "inline-block";
  } else {
    modalLink.style.display = "none";
  }

  newsModal.classList.add("open");
  document.body.style.overflow = "hidden"; // Orqa fon aylanib ketmasligi uchun
}

// 4. Modalni yopish
function closeModal() {
  newsModal.classList.remove("open");
  document.body.style.overflow = "auto";
}

closeModalBtn.addEventListener("click", closeModal);

// Modal tashqarisiga bosilganda ham yopilsin
newsModal.addEventListener("click", (e) => {
  if (e.target === newsModal) {
    closeModal();
  }
});

// ESC tugmasi bosilsa yopish
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && newsModal.classList.contains("open")) {
    closeModal();
  }
});

// 5. Kategoriya tugmalarini boshqarish
categoryButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    categoryButtons.forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    
    activeCategory = btn.getAttribute("data-category");
    renderNews();
  });
});

// Boshlash
initNewsListener();