import streamlit as st
import json
import os

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Vselix - Sınırsız Film ve Dizi",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DOSYA TABANLI VERİ YÖNETİMİ ---
DB_FILE = "movies.json"

default_movies = [
    {
        "id": "t1",
        "title": "Inception",
        "img": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=500&auto=format&fit=crop&q=80",
        "trailer": "https://www.youtube.com/watch?v=YoHD9XEInc0",
        "genre": "Bilim Kurgu • Aksiyon",
        "imdb": "8.8",
        "desc": "Rüya hırsızlığı yapan ve zihinlere fikir eken yetenekli bir hırsızın son görevi."
    },
    {
        "id": "t2",
        "title": "The Dark Knight",
        "img": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=500&auto=format&fit=crop&q=80",
        "trailer": "https://www.youtube.com/watch?v=EXeTwQWrcwY",
        "genre": "Aksiyon • Suç",
        "imdb": "9.0",
        "desc": "Batman, Gotham'ı kaosa sürükleyen Joker adlı suç dehasıyla yüzleşmek zorundadır."
    }
]

def load_movies():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        save_movies(default_movies)
        return default_movies

def save_movies(movies_list):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(movies_list, f, ensure_ascii=False, indent=4)

if "movies" not in st.session_state:
    st.session_state.movies = load_movies()

# --- CSS STİLLERİ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@400;600;700&display=swap');

    .stApp {
        background-color: #141414;
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
    }
    
    .vselix-logo {
        font-family: 'Bebas Neue', sans-serif;
        color: #E50914;
        font-size: 48px;
        letter-spacing: 3px;
        margin: 0;
        line-height: 1;
    }

    .hero-container {
        position: relative;
        background: linear-gradient(to top, #141414 10%, rgba(20,20,20,0.4) 60%),
                    url('https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=1400&auto=format&fit=crop&q=85');
        background-size: cover;
        background-position: center;
        height: 450px;
        border-radius: 10px;
        padding: 40px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        margin-bottom: 30px;
    }

    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 64px;
        letter-spacing: 2px;
        color: #FFFFFF;
        margin-bottom: 8px;
    }

    .row-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 26px;
        letter-spacing: 1px;
        margin-top: 30px;
        margin-bottom: 15px;
        color: #E5E5E5;
        border-left: 4px solid #E50914;
        padding-left: 10px;
    }

    div.stButton > button {
        background-color: #E50914;
        color: white;
        font-weight: 600;
        border-radius: 4px;
        border: none;
        padding: 10px 16px;
        width: 100%;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #F40612;
    }
    </style>
""", unsafe_allow_html=True)

# --- PROFİLLER VE YÖNETİCİ KONTROLÜ ---
if "profile" not in st.session_state:
    st.session_state.profile = None

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# --- 1. NETFLİX PROFİL SEÇİM EKRANI (Her cihazda ilk burası açılır) ---
if st.session_state.profile is None:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-family: Bebas Neue; font-size: 70px; color: #E50914; letter-spacing: 3px;'>VSELIX</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #fff; font-weight: 400; margin-bottom: 30px;'>Kim izliyor?</h3>", unsafe_allow_html=True)
    
    # Profil Butonları (Ortalanmış görünüm için sütunlar)
    col_emp1, c1, c2, c3, c_emp2 = st.columns([2, 1, 1, 1, 2])
    
    with c1:
        st.markdown("<div style='text-align: center; font-size: 40px;'>👨‍💻</div>", unsafe_allow_html=True)
        if st.button("Volkan"):
            st.session_state.profile = "Volkan"
            st.rerun()
            
    with c2:
        st.markdown("<div style='text-align: center; font-size: 40px;'>👩‍👩‍👦</div>", unsafe_allow_html=True)
        if st.button("Aile"):
            st.session_state.profile = "Aile"
            st.rerun()
            
    with c3:
        st.markdown("<div style='text-align: center; font-size: 40px;'>🍿</div>", unsafe_allow_html=True)
        if st.button("Misafir"):
            st.session_state.profile = "Misafir"
            st.rerun()

# --- 2. ANA UYGULAMA EKRANI (Profil seçildikten sonra açılır) ---
else:
    # Kenar Çubuğu (Yönetici Paneli ve Profil Değiştirme)
    with st.sidebar:
        st.markdown(f"### 👤 Aktif Profil: **{st.session_state.profile}**")
        if st.button("🔄 Profili Değiştir"):
            st.session_state.profile = None
            st.rerun()
        
        st.divider()
        st.markdown("### 🔐 Yönetici Paneli (Admin)")
        
        if not st.session_state.admin_logged:
            admin_pass = st.text_input("Yönetici Şifresi", type="password")
            if st.button("Giriş Yap"):
                if admin_pass == "vselix123": # Yönetici şifren
                    st.session_state.admin_logged = True
                    st.success("Giriş başarılı!")
                    st.rerun()
                else:
                    st.error("Hatalı şifre!")
        else:
            st.success("Yönetici olarak bağlandın! 🎬")
            if st.button("Admin Çıkışı Yap"):
                st.session_state.admin_logged = False
                st.rerun()
            
            st.markdown("---")
            st.subheader("➕ Yeni Film Ekle")
            new_title = st.text_input("Film Adı")
            new_genre = st.text_input("Tür (Örn: Aksiyon • Dram)")
            new_imdb = st.text_input("IMDb Puanı (Örn: 8.5)")
            new_img = st.text_input("Afiş Görsel Linki (URL)")
            new_trailer = st.text_input("YouTube Fragman Linki")
            new_desc = st.text_area("Film Özeti")
            
            if st.button("Filmi Sisteme Yükle"):
                if new_title and new_img:
                    new_movie = {
                        "id": str(len(st.session_state.movies) + 1),
                        "title": new_title,
                        "img": new_img,
                        "trailer": new_trailer if new_trailer else "https://www.youtube.com/watch?v=YoHD9XEInc0",
                        "genre": new_genre if new_genre else "Genel",
                        "imdb": new_imdb if new_imdb else "7.0",
                        "desc": new_desc if new_desc else "Açıklama girilmedi."
                    }
                    st.session_state.movies.append(new_movie)
                    save_movies(st.session_state.movies)
                    st.success(f"'{new_title}' başarıyla eklendi!")
                    st.rerun()
                else:
                    st.warning("Lütfen en az Film Adı ve Afiş Linkini doldurun.")

    # Üst Menü / Navbar
    col_logo, col_space, col_search = st.columns([2, 5, 3])

    with col_logo:
        st.markdown(f'<p class="vselix-logo">VSELIX</p>', unsafe_allow_html=True)

    with col_search:
        search_query = st.text_input("", placeholder="🔍 Film, dizi ara...", label_visibility="collapsed")

    st.markdown("<hr style='margin: 5px 0px 20px 0px; border-color: #333;'>", unsafe_allow_html=True)

    # Hero Banner
    st.markdown("""
        <div class="hero-container">
            <div style="background-color: rgba(229, 9, 20, 0.8); display: inline-block; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; width: fit-content; margin-bottom: 8px;">VSELIX ÖZEL YAPIM</div>
            <div class="hero-title">INTERSTELLAR</div>
            <div style="font-size: 15px; max-width: 580px; color: #D1D1D1; margin-bottom: 15px;">
                İnsanlığın son günlerinde bir grup astronot, yeni bir yaşanabilir gezegen bulmak için solucan deliğinden geçer.
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("▶ Hemen İzle (Fragman Oynat)", key="hero_play"):
        st.video("https://www.youtube.com/watch?v=zSWdZVtXT7E")

    st.divider()

    # Film Listeleme Fonksiyonu
    def display_movie_grid(movie_list):
        if not movie_list:
            st.info("Aradığınız kriterlere uygun içerik bulunamadı.")
            return

        cols_per_row = 4
        for i in range(0, len(movie_list), cols_per_row):
            row_movies = movie_list[i:i + cols_per_row]
            cols = st.columns(cols_per_row)
            
            for idx, movie in enumerate(row_movies):
                if search_query and search_query.lower() not in movie["title"].lower():
                    continue
                
                with cols[idx]:
                    st.image(movie["img"], use_container_width=True)
                    st.markdown(f"**{movie['title']}**")
                    st.caption(f"⭐ IMDb: {movie['imdb']} | {movie['genre']}")
                    
                    b_key = f"btn_{movie['id']}"
                    play_key = f"play_{movie['id']}"
                    
                    if st.button("▶ Fragman & Detay", key=b_key):
                        st.session_state[play_key] = not st.session_state.get(play_key, False)
                    
                    if st.session_state.get(play_key, False):
                        st.info(f"📌 **Özet:** {movie['desc']}")
                        st.video(movie["trailer"])

    # Kategoriler
    st.markdown('<div class="row-title">🔥 Vselix Arşivi ve Eklenen Filmler</div>', unsafe_allow_html=True)
    display_movie_grid(st.session_state.movies)