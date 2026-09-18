// Firebase SDK (Brauzer uchun CDN orqali)
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js";

// Sening Firebase loyihang sozlamalari
const firebaseConfig = {
  apiKey: "AIzaSyAbu2U2hH0PyUpGuy3bQyLabp0-oH2euhM",
  authDomain: "my-smart-news.firebaseapp.com",
  projectId: "my-smart-news",
  storageBucket: "my-smart-news.firebasestorage.app",
  messagingSenderId: "495823316961",
  appId: "1:495823316961:web:9ddb37c83fb37d505314a0",
  measurementId: "G-SMX48P8ZEM"
};

// Firebaseni ishga tushirish
const app = initializeApp(firebaseConfig);

// Firestore bazasini eksport qilish
export const db = getFirestore(app);