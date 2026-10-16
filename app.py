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

DB_FILE = "movies.json"
PROFILE_FILE = "profiles.json"

default_movies = [
    {
        "id": "dag2",
        "title": "Dağ 2",
        "img": "https://tr.web.img4.acsta.net/pictures/16/09/27/15/22/017772.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "genre": "Aksiyon • Savaş • Dram",
        "imdb": "8.9",
        "desc": "Birinci Özel Kuvvet Tugayı'na bağlı 8 kişilik Fırtına Getirenler Timi'nin hayatı ve sınır ötesi operasyonu.",
        "is_active": True
    },
    {
        "id": "furiosa",
        "title": "Furiosa: Bir Mad Max Destanı",
        "img": "https://tr.web.img4.acsta.net/pictures/24/03/19/12/12/3221371.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "genre": "Aksiyon • Bilim Kurgu • Macera",
        "imdb": "7.6",
        "desc": "Dünyanın çöküşünden yıllar sonra genç Furiosa, Yeşil Diyar'dan koparılır ve Savaş Lordu Dementus'un eline düşer.",
        "is_active": True
    },
    {
        "id": "ballerina",
        "title": "John Wick Dünyasından: Ballerina",
        "img": "https://tr.web.img4.acsta.net/pictures/24/09/26/15/28/1932645.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "genre": "Aksiyon • Gerilim",
        "imdb": "7.2",
        "desc": "John Wick evreninde geçen bu hikayede genç bir suikastçı, ailesinin intikamını almak için antik gelenekleri kullanıyor.",
        "is_active": True
    },
    {
        "id": "nefes",
        "title": "Nefes: Vatan Sağolsun",
        "img": "https://tr.web.img2.acsta.net/r_1280_720/pictures/bgt/04/72/47285.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "genre": "Savaş • Dram",
        "imdb": "8.0",
        "desc": "Güneydoğu Anadolu'daki bir karakolda görev yapan 40 asker ve komutanlarının zorlu yaşam mücadelesi.",
        "is_active": True
    },
    {
        "id": "t34",
        "title": "T-34",
        "img": "https://tr.web.img3.acsta.net/pictures/18/12/18/15/00/2219762.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "genre": "Aksiyon • Savaş • Tarih",
        "imdb": "6.7",
        "desc": "İkinci Dünya Savaşı sırasında esir düşen cesur bir Sovyet subayı, bir T-34 tankıyla imkansız bir kaçış planı yapar.",
        "is_active": True
    },
    {
        "id": "hellboy",
        "title": "Hellboy",
        "img": "https://tr.web.img4.acsta.net/pictures/19/03/01/10/58/0644342.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "genre": "Fantastik • Aksiyon • Macera",
        "imdb": "7.0",
        "desc": "Cehennemden gelen kırmızı iblis kahraman, dünyayı karanlık güçlerden korumak için amansız bir mücadele verir.",
        "is_active": True
    },
    {
        "id": "indiana",
        "title": "Indiana Jones: Kutsal Hazine Avcıları",
        "img": "https://tr.web.img4.acsta.net/pictures/21/04/14/15/22/0128795.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "genre": "Macera • Aksiyon",
        "imdb": "8.4",
        "desc": "Arkeolog Indiana Jones, Nazi güçlerinden önce Kutsal Kase'yi veya Ahit Sandığı'nı bulmak için tehlikeli bir maceraya atılır.",
        "is_active": True
    },
    {
        "id": "breach",
        "title": "Breach",
        "img": "https://tr.web.img4.acsta.net/pictures/20/11/17/12/03/4925766.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "genre": "Bilim Kurgu • Aksiyon",
        "imdb": "6.5",
        "desc": "Dünyayı terk eden bir gemide, uzaylı bir formun ele geçirdiği mürettebata karşı hayatta kalma savaşı.",
        "is_active": True
    },
    {
        "id": "dawn",
        "title": "Şafaktan Önce (Before Dawn)",
        "img": "https://tr.web.img3.acsta.net/pictures/22/08/17/11/49/0950663.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "genre": "Korku • Gerilim",
        "imdb": "6.2",
        "desc": "Karanlık çöktüğünde hayatta kalmaya çalışan bir grubun gerilim dolu ve ürkütücü hikayesi.",
        "is_active": True
    },
    {
        "id": "zombie",
        "title": "Ölülerin Dünyası: Zombi Günlükleri 2",
        "img": "https://tr.web.img2.acsta.net/pictures/fs/00/69/006992_ok.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "genre": "Korku • Aksiyon",
        "imdb": "5.8",
        "desc": "Zombi istilasından kaçmaya çalışan son insan kalıntılarının sığınak arayışı ve zombilere karşı amansız savaşı.",
        "is_active": True
    },
    {
        "id": "karacin",
        "title": "Kara Cin Laneti",
        "img": "https://tr.web.img2.acsta.net/pictures/24/02/13/14/50/2324673.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "genre": "Korku • Gizem",
        "imdb": "5.5",
        "desc": "Eski ve lanetli bir evin sırlarını araştırırken cinlerin hedefi haline gelen bir ailenin korku dolu anları.",
        "is_active": True
    }
] + [
    {
        "id": f"draft_{i+1}",
        "title": f"Taslak Slot #{i+1}",
        "img": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&auto=format&fit=crop&q=80",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "genre": "Taslak",
        "imdb": "0.0",
        "desc": "Bu film slotu henüz kapalı. Admin panelinden aktif yapabilirsiniz.",
        "is_active": False
    }
    for i in range(20)
]

default_profiles = [
    {"name": "Misafir", "color": "#eab308", "icon": "🍿"}
]

def save_data(filename, data_list):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

def load_data(filename, default_val):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except Exception:
            pass
    save_data(filename, default_val)
    return default_val

if "movies" not in st.session_state:
    st.session_state.movies = load_data(DB_FILE, default_movies)

if "profiles" not in st.session_state:
    st.session_state.profiles = load_data(PROFILE_FILE, default_profiles)

if "show_add_profile" not in st.session_state:
    st.session_state.show_add_profile = False

# --- MODERN VE PREMIUM CSS TASARIMI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        background-color: #0d0d0d;
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
    }
    
    .vselix-logo {
        font-family: 'Bebas Neue', sans-serif;
        color: #E50914;
        font-size: 56px;
        letter-spacing: 4px;
        margin: 0;
        line-height: 1;
        text-shadow: 0 4px 20px rgba(229, 9, 20, 0.6);
        transition: transform 0.3s ease;
    }

    .vselix-logo:hover {
        transform: scale(1.03);
    }

    .profile-card-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        cursor: pointer;
        margin-bottom: 20px;
    }

    .profile-avatar-box {
        width: 140px;
        height: 140px;
        border-radius: 12px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 58px;
        border: 3px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 8px 24px rgba(0,0,0,0.7);
        backdrop-filter: blur(10px);
    }

    .profile-card-container:hover .profile-avatar-box {
        border-color: #E50914;
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 12px 30px rgba(229, 9, 20, 0.5);
    }

    .profile-name {
        margin-top: 14px;
        font-size: 16px;
        color: #a3a3a3;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: color 0.2s;
    }

    .profile-card-container:hover .profile-name {
        color: #ffffff;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #E50914 0%, #b20710 100%);
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 14px;
        border-radius: 8px;
        border: none;
        padding: 12px 20px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.35);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        letter-spacing: 0.5px;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #ff1e27 0%, #E50914 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(229, 9, 20, 0.6);
    }

    .hero-container {
        position: relative;
        background: linear-gradient(180deg, rgba(13,13,13,0.1) 0%, rgba(13,13,13,0.95) 100%),
                    url('https://tr.web.img4.acsta.net/pictures/16/09/27/15/22/017772.jpg');
        background-size: cover;
        background-position: center 20%;
        height: 500px;
        border-radius: 16px;
        padding: 50px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        margin-bottom: 35px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .hero-badge {
        background: rgba(229, 9, 20, 0.9);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 11px;
        width: fit-content;
        margin-bottom: 12px;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 12px rgba(229, 9, 20, 0.4);
        backdrop-filter: blur(4px);
    }

    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 80px;
        letter-spacing: 3px;
        color: #FFFFFF;
        margin-bottom: 8px;
        line-height: 0.9;
        text-shadow: 0 4px 15px rgba(0,0,0,0.9);
    }

    .row-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 32px;
        letter-spacing: 1.5px;
        margin-top: 25px;
        margin-bottom: 20px;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    div[data-testid="column"] img {
        border-radius: 10px;
        transition: all 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
        cursor: pointer;
        box-shadow: 0 6px 18px rgba(0,0,0,0.5);
    }

    div[data-testid="column"] img:hover {
        transform: scale(1.06) translateY(-6px);
        box-shadow: 0 15px 30px rgba(229, 9, 20, 0.45);
        z-index: 50;
    }

    /* Streamlit Arama Kutusu Özelleştirme */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- OTURUM DURUMLARI ---
if "profile" not in st.session_state:
    st.session_state.profile = None

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

# --- 1. NETFLİX PROFİL SEÇİM EKRANI ---
if st.session_state.profile is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: Bebas Neue; font-size: 85px; text-align: center; color: #E50914; margin-bottom: 0; letter-spacing: 6px; text-shadow: 0 5px 25px rgba(229, 9, 20, 0.5);'>VSELIX</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #8c8c8c; font-weight: 500; margin-bottom: 45px; font-size: 24px; letter-spacing: 1px;'>Kim izliyor?</h3>", unsafe_allow_html=True)
    
    total_slots = len(st.session_state.profiles) + 1
    cols = st.columns(total_slots)
    
    for idx, prof in enumerate(st.session_state.profiles):
        with cols[idx]:
            bg_color = prof.get('color', '#333')
            icon = prof.get('icon', '👤')
            st.markdown(f"""
                <div class="profile-card-container">
                    <div class="profile-avatar-box" style="background-color: {bg_color};">{icon}</div>
                    <div class="profile-name">{prof['name']}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"👉 {prof['name']}", key=f"prof_btn_{idx}"):
                st.session_state.profile = prof['name']
                st.rerun()

    with cols[-1]:
        st.markdown(f"""
            <div class="profile-card-container">
                <div class="profile-avatar-box" style="background-color: rgba(255,255,255,0.03); border: 2px dashed rgba(255,255,255,0.2); color: #666;">+</div>
                <div class="profile-name">Profil Ekle</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("➕ Profil Ekle", key="add_prof_main_btn"):
            st.session_state.show_add_profile = True
            st.rerun()

    if st.session_state.show_add_profile:
        st.markdown("<br>", unsafe_allow_html=True)
        col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
        with col_f2:
            st.markdown("<h4 style='text-align: center; color: #fff;'>Yeni Profil Oluştur</h4>", unsafe_allow_html=True)
            with st.form("quick_add_profile"):
                new_name = st.text_input("Profil Adı")
                submitted = st.form_submit_button("Profili Kaydet")
                if submitted:
                    if new_name:
                        colors = ["#E50914", "#3b82f6", "#10b981", "#f97316", "#06b6d4", "#8b5cf6"]
                        import random
                        chosen_color = random.choice(colors)
                        st.session_state.profiles.append({"name": new_name, "color": chosen_color, "icon": "🍿"})
                        save_data(PROFILE_FILE, st.session_state.profiles)
                        st.session_state.show_add_profile = False
                        st.success(f"'{new_name}' başarıyla eklendi!")
                        st.rerun()
                    else:
                        st.warning("Lütfen bir profil adı girin.")

# --- 2. ANA UYGULAMA EKRANI ---
else:
    with st.sidebar:
        st.markdown(f"### 👤 Profil: **{st.session_state.profile}**")
        if st.button("🔄 Profili Değiştir"):
            st.session_state.profile = None
            st.rerun()
        
        st.divider()
        st.markdown("### ⚙️ Profil Yönetimi")
        with st.form("new_profile_form_sidebar"):
            new_p_name = st.text_input("Yeni Profil Adı")
            add_prof_btn = st.form_submit_button("Profil Ekle")
            if add_prof_btn:
                if new_p_name:
                    st.session_state.profiles.append({"name": new_p_name, "color": "#4f46e5", "icon": "🌟"})
                    save_data(PROFILE_FILE, st.session_state.profiles)
                    st.success(f"'{new_p_name}' profili eklendi!")
                    st.rerun()
                else:
                    st.warning("Lütfen profil adı girin.")

        if len(st.session_state.profiles) > 1:
            st.markdown("---")
            st.markdown("#### Profili Sil")
            profile_to_delete = st.selectbox("Silinecek Profili Seç", [p["name"] for p in st.session_state.profiles])
            if st.button("🗑️ Profili Kaldır"):
                st.session_state.profiles = [p for p in st.session_state.profiles if p["name"] != profile_to_delete]
                save_data(PROFILE_FILE, st.session_state.profiles)
                st.success("Profil silindi!")
                st.rerun()

        st.divider()
        st.markdown("### 🔐 Yönetici Paneli (Admin)")
        
        if not st.session_state.admin_logged:
            admin_pass = st.text_input("Yönetici Şifresi", type="password")
            if st.button("Giriş Yap"):
                if admin_pass == "vselix123":
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
            st.subheader("✏️ Film Yönetimi ve Düzenleme")
            
            movie_titles = [m["title"] for m in st.session_state.movies]
            selected_title = st.selectbox("Düzenlemek İstediğiniz Filmi Seçin", movie_titles)
            
            target_movie = next((m for m in st.session_state.movies if m["title"] == selected_title), None)
            
            if target_movie:
                with st.form("edit_movie_form"):
                    ed_active = st.checkbox("🟢 Yayın Durumu (Açık / Yayında)", value=target_movie.get("is_active", True))
                    ed_title = st.text_input("Film Adı", value=target_movie.get("title", ""))
                    ed_genre = st.text_input("Tür (Örn: Aksiyon • Dram)", value=target_movie.get("genre", ""))
                    ed_imdb = st.text_input("IMDb Puanı", value=target_movie.get("imdb", ""))
                    ed_img = st.text_input("Afiş Görsel Linki (URL)", value=target_movie.get("img", ""))
                    ed_video = st.text_input("Film Video Linki (Google Drive / Direct)", value=target_movie.get("video_url", ""))
                    ed_desc = st.text_area("Film Özeti", value=target_movie.get("desc", ""))
                    
                    update_btn = st.form_submit_button("💾 Filmi Kaydet ve Güncelle")
                    if update_btn:
                        target_movie["is_active"] = ed_active
                        target_movie["title"] = ed_title
                        target_movie["genre"] = ed_genre
                        target_movie["imdb"] = ed_imdb
                        target_movie["img"] = ed_img
                        target_movie["video_url"] = ed_video
                        target_movie["desc"] = ed_desc
                        
                        save_data(DB_FILE, st.session_state.movies)
                        st.success(f"'{ed_title}' başarıyla kaydedildi!")
                        st.rerun()

    # Navbar
    col_logo, col_space, col_search = st.columns([2, 5, 3])

    with col_logo:
        st.markdown('<p class="vselix-logo">VSELIX</p>', unsafe_allow_html=True)

    with col_search:
        search_query = st.text_input("", placeholder="🔍 Film, dizi ara...", label_visibility="collapsed")

    st.markdown("<hr style='margin: 10px 0px 25px 0px; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

    # Hero Banner
    st.markdown("""
        <div class="hero-container">
            <div class="hero-badge">VSELIX ÖZEL YAPIM</div>
            <div class="hero-title">DAĞ 2</div>
            <div style="font-size: 16px; max-width: 600px; color: #d1d1d1; margin-bottom: 15px; line-height: 1.5; font-weight: 400;">
                Birinci Özel Kuvvet Tugayı'na bağlı 8 kişilik Fırtına Getirenler Timi'nin sınır ötesi operasyonu ve destansı mücadelesi.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # SİNEMATİK DEV OYNATICI FONKSİYONU
    def render_custom_player(video_url):
        embed_url = video_url
        
        if "drive.google.com" in video_url:
            if "/file/d/" in video_url:
                file_id = video_url.split("/file/d/")[1].split("/")[0]
                embed_url = f"https://drive.google.com/file/d/{file_id}/preview"
            elif "id=" in video_url:
                file_id = video_url.split("id=")[1].split("&")[0]
                embed_url = f"https://drive.google.com/file/d/{file_id}/preview"

            player_html = f"""
            <div style="width:100%; display:flex; justify-content:center; margin:auto;">
                <iframe src="{embed_url}" width="100%" height="640" allow="autoplay; fullscreen" allowfullscreen="true" style="border:none; border-radius:12px; background:#000; box-shadow: 0 15px 35px rgba(0,0,0,0.9);"></iframe>
            </div>
            """
            st.components.v1.html(player_html, height=660)
        else:
            player_html = f"""
            <div style="width:100%; display:flex; justify-content:center; margin:auto;">
                <video controls autoplay style="width:100%; max-height:650px; border-radius:12px; background:#000; box-shadow: 0 15px 35px rgba(0,0,0,0.9);">
                    <source src="{video_url}" type="video/mp4">
                    <source src="{video_url}" type="video/ogg">
                    <source src="{video_url}" type="video/webm">
                    Tarayıcınız bu video formatını doğrudan desteklemiyor.
                </video>
            </div>
            """
            st.components.v1.html(player_html, height=670)

    # Film Listeleme Fonksiyonu
    def display_movie_grid(movie_list):
        visible_movies = [m for m in movie_list if m.get("is_active", True) or st.session_state.admin_logged]

        if not visible_movies:
            st.info("Yayında film bulunmuyor.")
            return

        cols_per_row = 4
        for i in range(0, len(visible_movies), cols_per_row):
            row_movies = visible_movies[i:i + cols_per_row]
            cols = st.columns(cols_per_row)
            
            for idx, movie in enumerate(row_movies):
                if search_query and search_query.lower() not in movie["title"].lower():
                    continue
                
                with cols[idx]:
                    st.image(movie["img"], use_container_width=True)
                    
                    if not movie.get("is_active", True):
                        st.markdown(f"**{movie['title']}** *(🔴 Taslak / Kapalı)*")
                    else:
                        st.markdown(f"**{movie['title']}**")
                        
                    st.caption(f"⭐ IMDb: {movie['imdb']} | {movie['genre']}")
                    
                    b_key = f"btn_{movie['id']}"
                    play_key = f"play_{movie['id']}"
                    
                    if st.button("▶ Filmi Başlat", key=b_key):
                        st.session_state[play_key] = not st.session_state.get(play_key, False)
                    
                    if st.session_state.get(play_key, False):
                        st.info(f"📌 **Özet:** {movie['desc']}")
                        v_url = movie.get("video_url", "")
                        render_custom_player(v_url)

    st.markdown('<div class="row-title">🎬 Vselix Film Arşivi</div>', unsafe_allow_html=True)
    display_movie_grid(st.session_state.movies)
