import streamlit as st
import json
import os
import random
import string

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Vselix - Sınırsız Film ve Dizi",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_FILE = "movies.json"
PROFILE_FILE = "profiles.json"
ACCESS_CODES_FILE = "access_codes.json"

default_movies = [
    {
        "id": "dag2",
        "title": "Dağ 2",
        "img": "https://tr.web.img4.acsta.net/pictures/16/09/27/15/22/017772.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "trailer_url": "https://www.youtube.com/watch?v=519u2895Djc",
        "genre": "Aksiyon",
        "imdb": "8.9",
        "desc": "Birinci Özel Kuvvet Tugayı'na bağlı 8 kişilik Fırtına Getirenler Timi'nin sınır ötesi operasyonu.",
        "is_active": True,
        "is_featured": True
    },
    {
        "id": "furiosa",
        "title": "Furiosa: Bir Mad Max Destanı",
        "img": "https://tr.web.img4.acsta.net/pictures/24/03/19/12/12/3221371.jpg",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "trailer_url": "https://www.youtube.com/watch?v=XJMek08brmg",
        "genre": "Bilim Kurgu",
        "imdb": "7.6",
        "desc": "Dünyanın çöküşünden yıllar sonra genç Furiosa, Yeşil Diyar'dan koparılır.",
        "is_active": True,
        "is_featured": False
    }
]

default_profiles = [
    {"name": "Misafir", "color": "#eab308", "icon": "🍿"}
]

default_codes = ["123456", "654321"]

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

if "access_codes" not in st.session_state:
    st.session_state.access_codes = load_data(ACCESS_CODES_FILE, default_codes)

if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

if "admin_logged" not in st.session_state:
    st.session_state.admin_logged = False

if "show_add_profile" not in st.session_state:
    st.session_state.show_add_profile = False

# --- CSS VE REALISTIC NETFLIX TASARIMI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        background-color: #141414;
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
    }
    
    .vselix-logo {
        font-family: 'Bebas Neue', sans-serif;
        color: #E50914;
        font-size: 64px;
        letter-spacing: 5px;
        margin: 0;
        line-height: 1;
        text-shadow: 0 4px 25px rgba(229, 9, 20, 0.7);
    }

    .netflix-login-card {
        background: rgba(0, 0, 0, 0.75);
        background-image: linear-gradient(to bottom, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.95) 100%);
        padding: 45px 40px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0,0,0,0.9);
        max-width: 480px;
        margin: 30px auto;
        backdrop-filter: blur(10px);
    }

    .netflix-header {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 55px;
        color: #E50914;
        letter-spacing: 3px;
        text-shadow: 0 0 15px rgba(229, 9, 20, 0.5);
        margin-bottom: 5px;
        text-align: center;
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
        border-radius: 8px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 58px;
        border: 3px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(0,0,0,0.7);
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
    }

    div.stButton > button {
        background: #E50914;
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 15px;
        border-radius: 4px;
        border: none;
        padding: 12px 20px;
        width: 100%;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4);
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background: #f6121d;
        transform: scale(1.01);
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.6);
    }

    .hero-container {
        position: relative;
        background-size: cover;
        background-position: center 20%;
        height: 520px;
        border-radius: 12px;
        padding: 50px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        margin-bottom: 35px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .hero-badge {
        background: #E50914;
        color: white;
        padding: 6px 14px;
        border-radius: 4px;
        font-weight: 800;
        font-size: 11px;
        width: fit-content;
        margin-bottom: 12px;
        letter-spacing: 1.5px;
    }

    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 85px;
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
    }
    
    .stTextInput input {
        background-color: #333333 !important;
        color: #ffffff !important;
        border-radius: 4px !important;
        border: none !important;
    }
    .stTextInput input:focus {
        border: 1px solid #E50914 !important;
    }
    </style>
""", unsafe_allow_html=True)

def format_youtube_embed(url):
    if "watch?v=" in url:
        v_id = url.split("watch?v=")[1].split("&")[0]
        return f"https://www.youtube.com/embed/{v_id}?autoplay=1"
    elif "youtu.be/" in url:
        v_id = url.split("youtu.be/")[1].split("?")[0]
        return f"https://www.youtube.com/embed/{v_id}?autoplay=1"
    elif "/embed/" in url:
        return url
    return url

# --- 1. AŞAMA: GİRİŞ EKRANI ---
if not st.session_state.is_authenticated:
    st.markdown("<br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    
    with col_l2:
        st.markdown("""
            <div class="netflix-login-card">
                <div class="netflix-header">VSELIX</div>
                <p style="color: #8c8c8c; font-size: 14px; text-align: center; margin-bottom: 25px;">Sınırsız film, dizi ve çok daha fazlası.</p>
            </div>
        """, unsafe_allow_html=True)
        
        tab_user, tab_admin = st.tabs(["🔑 Oturum Kodu (Aile)", "🔐 Yönetici Girişi (Admin)"])
        
        with tab_user:
            st.markdown("<p style='color: #b3b3b3; font-size: 13px; margin-top: 15px;'>Erişim için yetkiliyle iletişime geçip 6 haneli kodunuzu alın.</p>", unsafe_allow_html=True)
            with st.form("access_code_form"):
                user_code = st.text_input("6 Haneli Giriş Kodu", max_chars=6, placeholder="Örn: 123456")
                remember_me = st.checkbox("📌 Beni Hatırla (Bu cihazı kaydet)", value=True)
                submit_code = st.form_submit_button("Oturum Aç")
                
                if submit_code:
                    if user_code in st.session_state.access_codes:
                        st.session_state.is_authenticated = True
                        st.success("Giriş başarılı!")
                        st.rerun()
                    else:
                        st.error("❌ Geçersiz erişim kodu!")
                        
        with tab_admin:
            st.markdown("<p style='color: #b3b3b3; font-size: 13px; margin-top: 15px;'>Yönetici şifrenizle paneli doğrudan kontrol edin.</p>", unsafe_allow_html=True)
            with st.form("admin_login_form"):
                adm_pass = st.text_input("Yönetici Parolası", type="password", placeholder="Admin Parolası")
                submit_admin = st.form_submit_button("Yönetici Olarak Giriş Yap")
                
                if submit_admin:
                    if adm_pass == "vselix123":
                        st.session_state.is_authenticated = True
                        st.session_state.admin_logged = True
                        st.success("Yönetici girişi onaylandı!")
                        st.rerun()
                    else:
                        st.error("❌ Hatalı yönetici parolası!")

# --- 2. AŞAMA: PROFİL SEÇİM EKRANI ---
elif "profile" not in st.session_state or st.session_state.profile is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: Bebas Neue; font-size: 85px; text-align: center; color: #E50914; margin-bottom: 0; letter-spacing: 6px; text-shadow: 0 5px 25px rgba(229, 9, 20, 0.5);'>VSELIX</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #8c8c8c; font-weight: 500; margin-bottom: 45px; font-size: 24px;'>Kim izliyor?</h3>", unsafe_allow_html=True)
    
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
                        chosen_color = random.choice(colors)
                        st.session_state.profiles.append({"name": new_name, "color": chosen_color, "icon": "🍿"})
                        save_data(PROFILE_FILE, st.session_state.profiles)
                        st.session_state.show_add_profile = False
                        st.success(f"'{new_name}' eklendi!")
                        st.rerun()
                    else:
                        st.warning("Lütfen profil adı girin.")

# --- 3. AŞAMA: ANA UYGULAMA EKRANI ---
else:
    existing_genres = sorted(list(set(m.get("genre", "Aksiyon") for m in st.session_state.movies if m.get("genre"))))
    default_genre_options = ["Aksiyon", "Dram", "Komedi", "Bilim Kurgu", "Korku", "Animasyon", "Belgesel", "Macera", "Romantik"]
    combined_genres = sorted(list(set(existing_genres + default_genre_options))) + ["➕ Yeni Kategori Yaz / Ekle"]

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
                    st.success(f"'{new_p_name}' eklendi!")
                    st.rerun()

        if len(st.session_state.profiles) > 1:
            st.markdown("---")
            profile_to_delete = st.selectbox("Silinecek Profil", [p["name"] for p in st.session_state.profiles])
            if st.button("🗑️ Profili Sil"):
                st.session_state.profiles = [p for p in st.session_state.profiles if p["name"] != profile_to_delete]
                save_data(PROFILE_FILE, st.session_state.profiles)
                st.rerun()

        st.divider()
        st.markdown("### 🔐 Yönetici Paneli (Admin)")
        
        if not st.session_state.admin_logged:
            admin_pass = st.text_input("Yönetici Şifresi", type="password")
            if st.button("Giriş Yap"):
                if admin_pass == "vselix123":
                    st.session_state.admin_logged = True
                    st.success("Admin girişi yapıldı!")
                    st.rerun()
                else:
                    st.error("Hatalı şifre!")
        else:
            st.success("Yönetici Oturumu Aktif 🎬")
            if st.button("Admin Çıkışı Yap"):
                st.session_state.admin_logged = False
                st.rerun()
            
            st.markdown("---")
            st.subheader("🔑 Giriş Kodları Yönetimi")
            st.write("Aktif Kodlar:", st.session_state.access_codes)
            
            if st.button("🎲 Yeni Kod Üret"):
                new_c = ''.join(random.choices(string.digits, k=6))
                st.session_state.access_codes.append(new_c)
                save_data(ACCESS_CODES_FILE, st.session_state.access_codes)
                st.success(f"Yeni Kod: **{new_c}**")
                st.rerun()

            st.markdown("---")
            st.subheader("➕ Yeni Film Ekle")
            
            selected_genre_choice = st.selectbox("Kategori / Tür Seçin", combined_genres)
            custom_genre = ""
            if selected_genre_choice == "➕ Yeni Kategori Yaz / Ekle":
                custom_genre = st.text_input("Yeni Kategori İsmi", placeholder="Örn: Polisiye")

            with st.form("add_new_movie_form"):
                n_id = st.text_input("Film ID (İngilizce örn: mucize)")
                n_title = st.text_input("Film Adı")
                n_imdb = st.text_input("IMDb Puanı", value="7.0")
                n_img = st.text_input("Afiş Görsel URL")
                n_video = st.text_input("Video URL")
                n_trailer = st.text_input("YouTube Fragman URL")
                n_desc = st.text_area("Film Özeti")
                n_active = st.checkbox("🟢 Yayında (Herkes Görsün)", value=True)
                n_featured = st.checkbox("⭐ Öne Çıkan Film Yap", value=False)
                
                add_movie_btn = st.form_submit_button("🚀 Filmi Kaydet ve Yayınla")
                if add_movie_btn:
                    final_genre = custom_genre.strip() if selected_genre_choice == "➕ Yeni Kategori Yaz / Ekle" else selected_genre_choice
                    if n_id and n_title and final_genre:
                        if n_featured:
                            for m in st.session_state.movies:
                                m["is_featured"] = False

                        new_m = {
                            "id": n_id,
                            "title": n_title,
                            "img": n_img,
                            "video_url": n_video,
                            "trailer_url": n_trailer,
                            "genre": final_genre,
                            "imdb": n_imdb,
                            "desc": n_desc,
                            "is_active": n_active,
                            "is_featured": n_featured
                        }
                        st.session_state.movies.append(new_m)
                        save_data(DB_FILE, st.session_state.movies)
                        st.success(f"'{n_title}' başarıyla eklendi ve yayınlandı!")
                        st.rerun()
                    else:
                        st.warning("Eksik alanları doldurun.")

            st.markdown("---")
            st.subheader("✏️ Filmi Düzenle / Sil")
            movie_titles = [m["title"] for m in st.session_state.movies]
            selected_title = st.selectbox("Düzenlenecek Filmi Seç", movie_titles)
            
            target_movie = next((m for m in st.session_state.movies if m["title"] == selected_title), None)
            
            if target_movie:
                with st.form("edit_movie_form"):
                    ed_active = st.checkbox("🟢 Yayında (Herkes Görsün)", value=target_movie.get("is_active", True))
                    ed_featured = st.checkbox("⭐ Öne Çıkan Film Yap", value=target_movie.get("is_featured", False))
                    ed_title = st.text_input("Film Adı", value=target_movie.get("title", ""))
                    ed_genre = st.text_input("Kategori / Tür", value=target_movie.get("genre", ""))
                    ed_imdb = st.text_input("IMDb Puanı", value=target_movie.get("imdb", ""))
                    ed_img = st.text_input("Afiş Görsel Linki", value=target_movie.get("img", ""))
                    ed_video = st.text_input("Video Linki", value=target_movie.get("video_url", ""))
                    ed_trailer = st.text_input("Fragman Linki", value=target_movie.get("trailer_url", ""))
                    ed_desc = st.text_area("Özet", value=target_movie.get("desc", ""))
                    
                    update_btn = st.form_submit_button("💾 Güncellemeyi Kaydet")
                    if update_btn:
                        if ed_featured:
                            for m in st.session_state.movies:
                                m["is_featured"] = False

                        target_movie["is_active"] = ed_active
                        target_movie["is_featured"] = ed_featured
                        target_movie["title"] = ed_title
                        target_movie["genre"] = ed_genre
                        target_movie["imdb"] = ed_imdb
                        target_movie["img"] = ed_img
                        target_movie["video_url"] = ed_video
                        target_movie["trailer_url"] = ed_trailer
                        target_movie["desc"] = ed_desc
                        
                        save_data(DB_FILE, st.session_state.movies)
                        st.success("Film güncellendi!")
                        st.rerun()
                
                if st.button("🗑️ Bu Filmi Sil", key="del_movie_btn"):
                    st.session_state.movies = [m for m in st.session_state.movies if m["id"] != target_movie["id"]]
                    save_data(DB_FILE, st.session_state.movies)
                    st.rerun()

    # Navbar
    col_logo, col_space, col_search = st.columns([2, 3, 4])

    with col_logo:
        st.markdown('<p class="vselix-logo">VSELIX</p>', unsafe_allow_html=True)

    with col_search:
        search_query = st.text_input("", placeholder="🔍 Film, dizi veya kategori ara...", label_visibility="collapsed")

    st.markdown("<hr style='margin: 10px 0px 25px 0px; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

    # Hero Banner
    featured_movie = next((m for m in st.session_state.movies if m.get("is_featured", False) and (m.get("is_active", True) or st.session_state.admin_logged)), None)
    if not featured_movie:
        active_ones = [m for m in st.session_state.movies if m.get("is_active", True) or st.session_state.admin_logged]
        featured_movie = active_ones[0] if active_ones else st.session_state.movies[0]

    st.markdown(f"""
        <div class="hero-container" style="background: linear-gradient(180deg, rgba(20,20,20,0.1) 0%, rgba(20,20,20,0.95) 100%), url('{featured_movie['img']}');">
            <div class="hero-badge">⭐ VSELIX ÖNE ÇIKAN</div>
            <div class="hero-title">{featured_movie['title']}</div>
            <div style="font-size: 16px; max-width: 600px; color: #d1d1d1; margin-bottom: 15px; line-height: 1.5; font-weight: 400;">
                {featured_movie['desc']}
            </div>
        </div>
    """, unsafe_allow_html=True)

    def render_custom_player(video_url):
        if "drive.google.com" in video_url:
            embed_url = video_url
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
                    <source src="{video_url}" type="video/webm">
                    Tarayıcınız bu video formatını desteklemiyor.
                </video>
            </div>
            """
            st.components.v1.html(player_html, height=670)

    categories = sorted(list(set(m.get("genre", "Diğer") for m in st.session_state.movies if m.get("is_active", True) or st.session_state.admin_logged)))

    for cat in categories:
        cat_movies = [m for m in st.session_state.movies if m.get("genre", "Diğer") == cat and (m.get("is_active", True) or st.session_state.admin_logged)]
        
        if search_query:
            q = search_query.lower()
            cat_movies = [m for m in cat_movies if q in m["title"].lower() or q in m["genre"].lower()]

        if not cat_movies:
            continue

        st.markdown(f'<div class="row-title">📂 {cat}</div>', unsafe_allow_html=True)
        
        cols_per_row = 4
        for i in range(0, len(cat_movies), cols_per_row):
            row_movies = cat_movies[i:i + cols_per_row]
            cols = st.columns(cols_per_row)
            
            for idx, movie in enumerate(row_movies):
                with cols[idx]:
                    st.image(movie["img"], use_container_width=True)
                    
                    if not movie.get("is_active", True):
                        st.markdown(f"**{movie['title']}** *(🔴 Taslak)*")
                    else:
                        st.markdown(f"**{movie['title']}**")
                        
                    st.caption(f"⭐ IMDb: {movie['imdb']} | {movie['genre']}")
                    
                    b_key = f"btn_{movie['id']}"
                    t_key = f"tr_{movie['id']}"
                    play_key = f"play_{movie['id']}"
                    trailer_key = f"show_tr_{movie['id']}"
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        if st.button("▶ Oynat", key=b_key):
                            st.session_state[play_key] = not st.session_state.get(play_key, False)
                            st.session_state[trailer_key] = False
                    
                    with col_b2:
                        if st.button("🎬 Fragman", key=t_key):
                            st.session_state[trailer_key] = not st.session_state.get(trailer_key, False)
                            st.session_state[play_key] = False

                    if st.session_state.get(trailer_key, False):
                        t_raw = movie.get("trailer_url", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                        t_embed = format_youtube_embed(t_raw)
                        st.markdown(f"#### 🎬 {movie['title']} - Resmi Fragman")
                        st.components.v1.html(f"""
                            <iframe width="100%" height="400" src="{t_embed}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border-radius:10px;"></iframe>
                        """, height=420)

                    if st.session_state.get(play_key, False):
                        st.info(f"📌 **Özet:** {movie['desc']}")
                        v_url = movie.get("video_url", "")
                        render_custom_player(v_url)
