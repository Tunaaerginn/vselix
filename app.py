import streamlit as st
import json
import os
import random
import string
import requests
import base64

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

GITHUB_REPO = "Tunaaerginn/vselix"
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")

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
    }
]

default_profiles = [{"name": "Misafir", "color": "#E50914", "icon": "🍿"}]
default_codes = ["123456", "654321"]

def push_to_github(filename, data_list):
    """Veriyi GitHub Deposuna Otomatik Push Eder (Kalıcı Kayıt)"""
    if not GITHUB_TOKEN:
        return False
    
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    res = requests.get(url, headers=headers)
    sha = res.json().get("sha") if res.status_code == 200 else None
    
    content = json.dumps(data_list, ensure_ascii=False, indent=4)
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    
    payload = {
        "message": f"Auto-update {filename} via Vselix Admin Panel",
        "content": encoded_content
    }
    if sha:
        payload["sha"] = sha
        
    response = requests.put(url, headers=headers, json=payload)
    return response.status_code in [200, 201]

def save_data(filename, data_list):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
    push_to_github(filename, data_list)

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

# --- ULTRA KOZMETİK CSS VE İNTERAKTİF PROFİL KARTLARI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    .stApp {
        background: #0f0f12;
        background-image: radial-gradient(circle at 50% -20%, #1f080a 0%, #0f0f12 80%);
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    
    .vselix-logo {
        font-family: 'Bebas Neue', sans-serif;
        color: #E50914;
        font-size: 72px;
        letter-spacing: 6px;
        margin: 0;
        line-height: 1;
        text-shadow: 0 0 30px rgba(229, 9, 20, 0.6), 0 0 60px rgba(229, 9, 20, 0.2);
    }

    .netflix-login-card {
        background: rgba(18, 18, 22, 0.75);
        padding: 50px 45px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 30px 60px rgba(0,0,0,0.8);
        max-width: 480px;
        margin: 40px auto;
        backdrop-filter: blur(20px);
    }

    .netflix-header {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 60px;
        color: #E50914;
        letter-spacing: 4px;
        text-shadow: 0 0 20px rgba(229, 9, 20, 0.5);
        margin-bottom: 5px;
        text-align: center;
    }

    /* Profil Seçim Butonu Özelleştirmesi (Direk Kutuya Tıklama Hissi) */
    div.stButton > button {
        background: linear-gradient(135deg, #E50914 0%, #b20710 100%);
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 15px;
        border-radius: 8px;
        border: none;
        padding: 12px 22px;
        width: 100%;
        box-shadow: 0 4px 20px rgba(229, 9, 20, 0.35);
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #f6121d 0%, #d60914 100%);
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 8px 25px rgba(229, 9, 20, 0.6);
    }

    /* Profil Kartı Özel Stili */
    .profile-card-box {
        background: rgba(255, 255, 255, 0.02);
        border: 2px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
        margin-bottom: 10px;
    }
    .profile-card-box:hover {
        border-color: #E50914;
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(229, 9, 20, 0.4);
    }

    .hero-container {
        position: relative;
        background-size: cover;
        background-position: center 25%;
        height: 540px;
        border-radius: 20px;
        padding: 60px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        margin-bottom: 40px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.9);
        border: 1px solid rgba(255, 255, 255, 0.1);
        overflow: hidden;
    }

    .hero-badge {
        background: rgba(229, 9, 20, 0.9);
        backdrop-filter: blur(8px);
        color: white;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 800;
        font-size: 12px;
        width: fit-content;
        margin-bottom: 14px;
        letter-spacing: 2px;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4);
    }

    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 90px;
        letter-spacing: 4px;
        color: #FFFFFF;
        margin-bottom: 10px;
        line-height: 0.9;
        text-shadow: 0 5px 25px rgba(0,0,0,0.95);
    }

    .row-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 34px;
        letter-spacing: 2px;
        margin-top: 35px;
        margin-bottom: 20px;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        padding: 12px 16px !important;
    }
    .stTextInput input:focus {
        border-color: #E50914 !important;
        box-shadow: 0 0 15px rgba(229, 9, 20, 0.3) !important;
    }

    .imdb-badge {
        background: #f5c518;
        color: #000;
        font-weight: 900;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 12px;
        display: inline-block;
        margin-right: 6px;
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
                <p style="color: #a3a3a3; font-size: 15px; text-align: center; margin-bottom: 30px;">Sınırsız film, dizi ve özel içerik dünyası.</p>
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

# --- 2. AŞAMA: PROFİL SEÇİM EKRANI (DOĞRUDAN PROFİLE TIKLAMA) ---
elif "profile" not in st.session_state or st.session_state.profile is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: Bebas Neue; font-size: 95px; text-align: center; color: #E50914; margin-bottom: 0; letter-spacing: 8px; text-shadow: 0 5px 35px rgba(229, 9, 20, 0.6);'>VSELIX</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #a3a3a3; font-weight: 500; margin-bottom: 50px; font-size: 26px;'>Kim izliyor?</h3>", unsafe_allow_html=True)
    
    total_slots = len(st.session_state.profiles) + 1
    cols = st.columns(total_slots)
    
    for idx, prof in enumerate(st.session_state.profiles):
        with cols[idx]:
            bg_color = prof.get('color', '#333')
            icon = prof.get('icon', '👤')
            
            # Şık Profil Kutusu Görseli
            st.markdown(f"""
                <div class="profile-card-box">
                    <div style="width: 120px; height: 120px; border-radius: 16px; background-color: {bg_color}; display: flex; justify-content: center; align-items: center; font-size: 52px; margin: 0 auto; box-shadow: 0 8px 25px rgba(0,0,0,0.6);">
                        {icon}
                    </div>
                    <div style="margin-top: 15px; font-size: 18px; color: #ffffff; font-weight: 700;">{prof['name']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Doğrudan profili seçme butonu
            if st.button(f"✨ {prof['name']} ile İzle", key=f"prof_btn_{idx}"):
                st.session_state.profile = prof['name']
                st.rerun()

    with cols[-1]:
        st.markdown(f"""
            <div class="profile-card-box" style="border: 2px dashed rgba(255,255,255,0.2);">
                <div style="width: 120px; height: 120px; border-radius: 16px; background: rgba(255,255,255,0.03); display: flex; justify-content: center; align-items: center; font-size: 52px; margin: 0 auto; color: #777;">
                    +
                </div>
                <div style="margin-top: 15px; font-size: 18px; color: #888; font-weight: 700;">Yeni Profil</div>
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
                        st.success(f"'{n_title}' eklendi ve GitHub'a kaydedildi!")
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
                        st.success("Film güncellendi ve GitHub'a kaydedildi!")
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

    st.markdown("<hr style='margin: 15px 0px 30px 0px; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

    # Hero Banner
    featured_movie = next((m for m in st.session_state.movies if m.get("is_featured", False) and (m.get("is_active", True) or st.session_state.admin_logged)), None)
    if not featured_movie:
        active_ones = [m for m in st.session_state.movies if m.get("is_active", True) or st.session_state.admin_logged]
        featured_movie = active_ones[0] if active_ones else st.session_state.movies[0]

    st.markdown(f"""
        <div class="hero-container" style="background: linear-gradient(180deg, rgba(15,15,18,0.1) 0%, rgba(15,15,18,0.98) 100%), url('{featured_movie['img']}');">
            <div class="hero-badge">🔥 VSELIX ÖNE ÇIKAN</div>
            <div class="hero-title">{featured_movie['title']}</div>
            <div style="font-size: 16px; max-width: 650px; color: #d1d1d1; margin-bottom: 20px; line-height: 1.6; font-weight: 400;">
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
                <iframe src="{embed_url}" width="100%" height="640" allow="autoplay; fullscreen" allowfullscreen="true" style="border:none; border-radius:16px; background:#000; box-shadow: 0 20px 40px rgba(0,0,0,0.9);"></iframe>
            </div>
            """
            st.components.v1.html(player_html, height=660)
        else:
            player_html = f"""
            <div style="width:100%; display:flex; justify-content:center; margin:auto;">
                <video controls autoplay style="width:100%; max-height:650px; border-radius:16px; background:#000; box-shadow: 0 20px 40px rgba(0,0,0,0.9);">
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

        st.markdown(f'<div class="row-title">🎬 {cat}</div>', unsafe_allow_html=True)
        
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
                        
                    st.markdown(f'<span class="imdb-badge">IMDb</span> **{movie["imdb"]}**', unsafe_allow_html=True)
                    
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
                            <iframe width="100%" height="400" src="{t_embed}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="border-radius:12px;"></iframe>
                        """, height=420)

                    if st.session_state.get(play_key, False):
                        st.info(f"📌 **Özet:** {movie['desc']}")
                        v_url = movie.get("video_url", "")
                        render_custom_player(v_url)
