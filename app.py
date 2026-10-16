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
PROFILE_FILE = "profiles.json"

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

# NETFLİX ORİJİNAL RENKLİ PROFIL AVATARLARI (İnsan resimleri tamamen kaldırıldı)
default_avatar = "https://upload.wikimedia.org/wikipedia/commons/0/0b/Netflix-avatar.png"

default_profiles = [
    {"name": "Volkan", "avatar": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Netflix-avatar.png"},
    {"name": "Aile", "avatar": "https://mir-s3-cdn-cf.behance.net/project_modules/disp/84c20033850498.56ba69ac290ea.png"},
    {"name": "Misafir", "avatar": "https://mir-s3-cdn-cf.behance.net/project_modules/disp/64623a33850498.56ba69ac2a6f7.png"}
]

def save_data(filename, data_list):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

def load_data(filename, default_val):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    save_data(filename, default_val)
                    return default_val
                data = json.loads(content)
                # Eski insan resimleri kalmışsa otomatik temizle
                if filename == PROFILE_FILE:
                    for p in data:
                        if "unsplash.com" in p.get("avatar", ""):
                            p["avatar"] = default_avatar
                return data
        except Exception:
            save_data(filename, default_val)
            return default_val
    else:
        save_data(filename, default_val)
        return default_val

if "movies" not in st.session_state:
    st.session_state.movies = load_data(DB_FILE, default_movies)

if "profiles" not in st.session_state:
    st.session_state.profiles = load_data(PROFILE_FILE, default_profiles)

if "show_add_profile" not in st.session_state:
    st.session_state.show_add_profile = False

# --- NETFLİX CSS & TASARIM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@400;500;600;700&display=swap');

    .stApp {
        background-color: #141414;
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
    }
    
    .vselix-logo {
        font-family: 'Bebas Neue', sans-serif;
        color: #E50914;
        font-size: 52px;
        letter-spacing: 3px;
        margin: 0;
        line-height: 1;
        text-shadow: 0 2px 10px rgba(229, 9, 20, 0.4);
    }

    /* Giriş Animasyonu */
    .net-intro {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: #000000;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 99999;
        animation: fadeOut 0.4s ease 1.2s forwards;
    }

    @keyframes fadeOut {
        to { opacity: 0; visibility: hidden; }
    }

    .intro-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 130px;
        color: #E50914;
        letter-spacing: 10px;
        animation: scaleUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    @keyframes scaleUp {
        0% { transform: scale(0.4); opacity: 0; filter: blur(10px); }
        60% { transform: scale(1.08); opacity: 1; filter: blur(0px); }
        100% { transform: scale(1); opacity: 1; }
    }

    /* NETFLİX PROFİL SEÇİM EKRANI STİLLERİ */
    .profile-box {
        text-align: center;
        cursor: pointer;
    }

    .profile-avatar {
        width: 135px;
        height: 135px;
        border-radius: 6px;
        object-fit: cover;
        border: 3px solid transparent;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.6);
        background-color: #333;
    }

    .profile-box:hover .profile-avatar {
        border-color: #ffffff;
        transform: scale(1.05);
        box-shadow: 0 8px 22px rgba(229, 9, 20, 0.5);
    }

    .profile-title {
        margin-top: 12px;
        font-size: 16px;
        color: #b3b3b3;
        font-weight: 500;
        letter-spacing: 0.5px;
    }

    .profile-box:hover .profile-title {
        color: #ffffff;
    }

    /* Artı Butonu Kutusu */
    .add-profile-icon {
        width: 135px;
        height: 135px;
        border-radius: 6px;
        border: 3px dashed #666;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 55px;
        color: #666;
        background-color: rgba(255,255,255,0.03);
        transition: all 0.2s ease;
    }

    .profile-box:hover .add-profile-icon {
        border-color: #fff;
        color: #fff;
        background-color: rgba(255,255,255,0.08);
        transform: scale(1.05);
    }

    /* Hero Banner */
    .hero-container {
        position: relative;
        background: linear-gradient(to top, #141414 10%, rgba(20,20,20,0.3) 60%),
                    url('https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=1400&auto=format&fit=crop&q=85');
        background-size: cover;
        background-position: center;
        height: 480px;
        border-radius: 8px;
        padding: 45px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        margin-bottom: 25px;
        box-shadow: inset 0 0 100px rgba(0,0,0,0.8);
    }

    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 70px;
        letter-spacing: 2px;
        color: #FFFFFF;
        margin-bottom: 6px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.9);
    }

    .row-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 28px;
        letter-spacing: 1px;
        margin-top: 35px;
        margin-bottom: 15px;
        color: #E5E5E5;
    }

    /* Film Kartları Hover Efekti */
    div[data-testid="column"] img {
        border-radius: 6px;
        transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s ease;
        cursor: pointer;
    }

    div[data-testid="column"] img:hover {
        transform: scale(1.08);
        box-shadow: 0 12px 25px rgba(229, 9, 20, 0.5);
        z-index: 50;
    }

    /* Butonlar */
    div.stButton > button {
        background-color: #E50914;
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        font-size: 14px;
        border-radius: 6px;
        border: none;
        padding: 10px 18px;
        width: 100%;
        box-shadow: 0 4px 12px rgba(229, 9, 20, 0.3);
        transition: all 0.25s ease;
    }

    div.stButton > button:hover {
        background-color: #F40612;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(229, 9, 20, 0.5);
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
    st.markdown("""
        <div class="net-intro">
            <div class="intro-title">VSELIX</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-family: Bebas Neue; font-size: 75px; text-align: center; color: #E50914; margin-bottom: 0; letter-spacing: 4px;'>VSELIX</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #b3b3b3; font-weight: 400; margin-bottom: 30px; font-size: 26px;'>Kim izliyor?</h3>", unsafe_allow_html=True)
    
    total_slots = len(st.session_state.profiles) + 1
    cols = st.columns(total_slots)
    
    for idx, prof in enumerate(st.session_state.profiles):
        with cols[idx]:
            st.markdown(f"""
                <div class="profile-box" style="display: flex; flex-direction: column; align-items: center;">
                    <img src="{prof['avatar']}" class="profile-avatar">
                    <div class="profile-title">{prof['name']}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Seç: {prof['name']}", key=f"prof_btn_{idx}"):
                st.session_state.profile = prof['name']
                st.rerun()

    # En sağdaki "+" Profil Ekle Butonu
    with cols[-1]:
        st.markdown(f"""
            <div class="profile-box" style="display: flex; flex-direction: column; align-items: center;">
                <div class="add-profile-icon">+</div>
                <div class="profile-title">Profil Ekle</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("➕ Profil Ekle", key="add_prof_main_btn"):
            st.session_state.show_add_profile = True
            st.rerun()

    # Profil Ekleme Form Alanı
    if st.session_state.show_add_profile:
        st.markdown("<br>", unsafe_allow_html=True)
        col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
        with col_f2:
            st.markdown("<h4 style='text-align: center; color: #fff;'>Yeni Profil Oluştur</h4>", unsafe_allow_html=True)
            with st.form("quick_add_profile"):
                new_name = st.text_input("Profil Adı")
                new_avatar = st.text_input("Profil Fotoğrafı URL (Boş bırakırsan varsayılan kırmızı ikon atanır)")
                submitted = st.form_submit_button("Profili Kaydet")
                if submitted:
                    if new_name:
                        avatar_url = new_avatar if new_avatar.strip() != "" else default_avatar
                        st.session_state.profiles.append({"name": new_name, "avatar": avatar_url})
                        save_data(PROFILE_FILE, st.session_state.profiles)
                        st.session_state.show_add_profile = False
                        st.success(f"'{new_name}' başarıyla eklendi!")
                        st.rerun()
                    else:
                        st.warning("Lütfen bir profil adı girin.")

# --- 2. ANA UYGULAMA EKRANI ---
else:
    with st.sidebar:
        st.markdown(f"### 👤 Aktif Profil: **{st.session_state.profile}**")
        if st.button("🔄 Profili Değiştir"):
            st.session_state.profile = None
            st.rerun()
        
        st.divider()
        st.markdown("### ⚙️ Profil Yönetimi")
        with st.form("new_profile_form_sidebar"):
            new_p_name = st.text_input("Yeni Profil Adı")
            new_p_avatar = st.text_input("Avatar URL (İsteğe bağlı)", placeholder="https://...")
            add_prof_btn = st.form_submit_button("Profil Ekle")
            if add_prof_btn:
                if new_p_name:
                    avatar_url = new_p_avatar if new_p_avatar.strip() != "" else default_avatar
                    st.session_state.profiles.append({"name": new_p_name, "avatar": avatar_url})
                    save_data(PROFILE_FILE, st.session_state.profiles)
                    st.success(f"'{new_p_name}' profili eklendi!")
                    st.rerun()
                else:
                    st.warning("Lütfen profil adı girin.")

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
                    save_data(DB_FILE, st.session_state.movies)
                    st.success(f"'{new_title}' başarıyla eklendi!")
                    st.rerun()
                else:
                    st.warning("Lütfen en az Film Adı ve Afiş Linkini doldurun.")

    # Üst Menü / Navbar
    col_logo, col_space, col_search = st.columns([2, 5, 3])

    with col_logo:
        st.markdown('<p class="vselix-logo">VSELIX</p>', unsafe_allow_html=True)

    with col_search:
        search_query = st.text_input("", placeholder="🔍 Film, dizi ara...", label_visibility="collapsed")

    st.markdown("<hr style='margin: 5px 0px 20px 0px; border-color: #222;'>", unsafe_allow_html=True)

    # Hero Banner
    st.markdown("""
        <div class="hero-container">
            <div style="background-color: #E50914; display: inline-block; padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 11px; width: fit-content; margin-bottom: 8px; letter-spacing: 1px;">VSELIX ÖZEL YAPIM</div>
            <div class="hero-title">INTERSTELLAR</div>
            <div style="font-size: 15px; max-width: 580px; color: #D1D1D1; margin-bottom: 15px; line-height: 1.4;">
                İnsanlığın son günlerinde bir grup astronot, yeni bir yaşanabilir gezegen bulmak için solucan deliğinden geçer.
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("▶ Hemen İzle (Fragman Oynat
