import streamlit as st
import fitz
from groq import Groq
from dotenv import load_dotenv
import os
import json
 
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
st.set_page_config(
    page_title="AI Study Companion",
    page_icon="🎓",
    layout="wide"
)
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
 
* { font-family: 'Inter', sans-serif; }
 
.main {
    background: linear-gradient(160deg, #f0f4ff 0%, #faf0ff 50%, #f0fff8 100%);
    min-height: 100vh;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #f0f4ff 0%, #faf0ff 50%, #f0fff8 100%);
}
[data-testid="stHeader"] {
    background: transparent;
}
.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 40px;
    color: white;
    margin-bottom: 30px;
}
.hero h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    color: white !important;
    -webkit-text-fill-color: white !important;
}
.hero p {
    font-size: 1.1rem;
    opacity: 0.9;
    margin: 10px 0 0;
}
div.stButton > button {
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    border: none;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    transition: all 0.2s ease;
    width: 100%;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px 10px 0 0;
    font-weight: 600;
    padding: 10px 24px;
}
.stat-box {
    background: white;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 15px rgba(0,0,0,0.06);
    border: 1px solid #eee;
}
.stat-number {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-label {
    font-size: 0.85rem;
    color: #888;
    margin-top: 4px;
}
.result-box {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 15px rgba(0,0,0,0.06);
    border: 1px solid #eee;
    margin-top: 16px;
}
</style>
""", unsafe_allow_html=True)
 
st.markdown("""
<div class="hero">
    <h1>🎓 AI Study Companion</h1>
    <p>PDF ders notlarini yapay zeka ile analiz et, ozetle, quiz coz ve flashcard calis.</p>
</div>
""", unsafe_allow_html=True)
 
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:20px 0;">
        <div style="font-size:3rem;">🎓</div>
        <h2 style="background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:8px 0;">AI Study Companion</h2>
        <p style="color:#888;font-size:0.85rem;">Yapay zeka destekli calisma asistani</p>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("---")
    st.markdown("#### 📄 PDF Yukle")
    uploaded_files = st.file_uploader("PDF sec", type="pdf", accept_multiple_files=True, label_visibility="collapsed")
 
    if uploaded_files:
        pdf_isimleri = [f.name for f in uploaded_files]
        secili_pdf = st.selectbox("Aktif PDF:", pdf_isimleri)
        uploaded_file = next(f for f in uploaded_files if f.name == secili_pdf)
 
        if "gecmis" not in st.session_state:
            st.session_state["gecmis"] = []
        if uploaded_file.name not in st.session_state["gecmis"]:
            st.session_state["gecmis"].insert(0, uploaded_file.name)
            if len(st.session_state["gecmis"]) > 5:
                st.session_state["gecmis"] = st.session_state["gecmis"][:5]
 
        st.success(f"✓ {len(uploaded_files)} PDF yuklendi")
    else:
        uploaded_file = None
 
    st.markdown("---")
 
    if "gecmis" in st.session_state and st.session_state["gecmis"]:
        st.markdown("#### 🕓 Son Yuklenenler")
        for isim in st.session_state["gecmis"]:
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:10px 14px;margin:6px 0;font-size:0.85rem;color:#555;border:1px solid #eee;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                📄 {isim}
            </div>
            """, unsafe_allow_html=True)
 
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;color:#bbb;font-size:0.75rem;">
        Made with ❤️ using Groq & Streamlit
    </div>
    """, unsafe_allow_html=True)
 
if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    metin = ""
    for sayfa in doc:
        metin += sayfa.get_text()
 
    temiz_metin = ""
    for karakter in metin:
        if ord(karakter) < 128 or karakter in "çğışöüÇĞİŞÖÜ":
            temiz_metin += karakter
    metin = temiz_metin
 
    kelime_sayisi = len(metin.split())
    st.markdown(f"""
    <div style="display:flex; gap:16px; margin:20px 0;">
        <div class="stat-box" style="flex:1">
            <div class="stat-number">{len(doc)}</div>
            <div class="stat-label">Sayfa</div>
        </div>
        <div class="stat-box" style="flex:1">
            <div class="stat-number">{kelime_sayisi}</div>
            <div class="stat-label">Kelime</div>
        </div>
        <div class="stat-box" style="flex:1">
            <div class="stat-number">{len(metin)}</div>
            <div class="stat-label">Karakter</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
    sekme1, sekme2, sekme3, sekme4, sekme5 = st.tabs(["📝 Ozetle", "❓ Quiz", "🃏 Flashcard", "💬 Sohbet", "🧠 Analiz"])
 
    with sekme1:
        st.subheader("Anlatim modunu sec")
        mod = st.selectbox("Mod", [
            "Normal ozet",
            "Arkadas gibi anlat",
            "Teknik / muhendislik anlatimi",
            "Cok kisa ozet",
            "Sinav modu",
            "Son gece tekrar modu"
        ])
 
        if st.button("Ozetle", key="ozetle_btn"):
            if mod == "Normal ozet":
                sistem = "Sen bir universite hocasisin. Ogrenciye ders anlatir gibi, akilda kalici sekilde ozetle. Teknik terimleri orijinal dilde birak. Turkce anlat."
                prompt = f"Su ders notunu ogrencinin kafasina girecek sekilde ozetle:\n\n{metin}"
            elif mod == "Arkadas gibi anlat":
                sistem = "Sen samimi bir arkadas gibi konusuyorsun. Eglenceli ol. Teknik terimleri orijinal dilde birak. Turkce anlat."
                prompt = f"Su konuyu bana arkadas gibi, eglenceli anlat:\n\n{metin}"
            elif mod == "Teknik / muhendislik anlatimi":
                sistem = "Sen teknik bir uzmansin. Detayli, terimlerle, profesyonel bir dille anlat. Tum teknik terimler orijinal dilinde kalmali."
                prompt = f"Su konuyu teknik olarak anlat:\n\n{metin}"
            elif mod == "Cok kisa ozet":
                sistem = "Cok kisa ve oz yaz. Maksimum 5 madde. Teknik terimleri orijinal dilde birak."
                prompt = f"Su metni 5 maddede ozetle:\n\n{metin}"
            elif mod == "Sinav modu":
                sistem = "Ogrencinin sinava hazirlanmasina yardim ediyorsun. En onemli konulari vurgula. Teknik terimleri orijinal dilde birak."
                prompt = f"Bu metinden sinava girecek biri icin en kritik bilgileri cikar:\n\n{metin}"
            elif mod == "Son gece tekrar modu":
                sistem = "Ogrencinin sinava az vakti kaldi. En kritik bilgileri madde madde ver. Teknik terimleri orijinal dilde birak."
                prompt = f"Sinava bir gecem var, ne ezberlemeliyim:\n\n{metin}"
 
            with st.spinner("Yapay zeka ozetliyor..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": sistem},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.write(response.choices[0].message.content)
                st.markdown('</div>', unsafe_allow_html=True)
 
    with sekme2:
        st.subheader("Quiz olustur")
        soru_sayisi = st.slider("Kac soru olsun?", 3, 10, 5)
 
        if st.button("Quiz Olustur", key="quiz_btn"):
            with st.spinner("Sorular hazirlaniyor..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": """Sen bir ogretmensin. Sadece JSON formatinda cevap veriyorsun.
Format:
[
  {
    "soru": "Soru metni",
    "secenekler": ["A) ...", "B) ...", "C) ...", "D) ..."],
    "dogru": "A"
  }
]"""},
                        {"role": "user", "content": f"Su metinden {soru_sayisi} adet coktan secmeli soru olustur. Teknik terimleri orijinal dilde birak:\n\n{metin}"}
                    ]
                )
                ham_cevap = response.choices[0].message.content.strip()
                if ham_cevap.startswith("```"):
                    ham_cevap = ham_cevap.split("```")[1]
                    if ham_cevap.startswith("json"):
                        ham_cevap = ham_cevap[4:]
                ham_cevap = ham_cevap.strip()
 
                try:
                    sorular = json.loads(ham_cevap)
                    st.session_state["sorular"] = sorular
                    st.session_state["cevaplar"] = {}
                    st.session_state["kontrol"] = False
                except:
                    st.error("Sorular yuklenemedi, tekrar dene.")
 
        if "sorular" in st.session_state and st.session_state["sorular"]:
            sorular = st.session_state["sorular"]
 
            for i, soru in enumerate(sorular):
                st.markdown("---")
                st.markdown(f"**Soru {i+1}: {soru['soru']}**")
                secim = st.radio(
                    "Secenek",
                    soru["secenekler"],
                    key=f"soru_{i}",
                    label_visibility="collapsed"
                )
                st.session_state["cevaplar"][i] = secim[0]
 
                if st.session_state.get("kontrol"):
                    kullanici = st.session_state["cevaplar"].get(i, "")
                    dogru = soru["dogru"]
                    if kullanici == dogru:
                        st.success("Dogru!")
                    else:
                        dogru_secenekler = [s for s in soru["secenekler"] if s.startswith(dogru)]
                        dogru_secenek = dogru_secenekler[0] if dogru_secenekler else dogru
                        st.error(f"Yanlis! Dogru cevap: {dogru_secenek}")
 
            if st.button("Cevaplari Kontrol Et", key="kontrol_btn"):
                st.session_state["kontrol"] = True
                st.rerun()
 
            if st.session_state.get("kontrol"):
                dogru_sayisi = sum(
                    1 for i, soru in enumerate(sorular)
                    if st.session_state["cevaplar"].get(i, "") == soru["dogru"]
                )
                st.markdown("---")
                st.markdown(f"### Toplam Skor: {dogru_sayisi}/{len(sorular)}")
 
    with sekme3:
        st.subheader("Flashcard olustur")
        kart_sayisi = st.slider("Kac kart olsun?", 3, 15, 8)
 
        if st.button("Kartlari Olustur", key="kart_btn"):
            with st.spinner("Kartlar hazirlaniyor..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": """Sen bir ogretmensin. Sadece JSON formatinda cevap veriyorsun.
Format:
[
  {
    "on": "Kavram veya soru",
    "arka": "Tanim veya cevap"
  }
]"""},
                        {"role": "user", "content": f"Su metinden {kart_sayisi} adet flashcard olustur. Teknik terimleri orijinal dilde birak:\n\n{metin}"}
                    ]
                )
                ham_cevap = response.choices[0].message.content.strip()
                if ham_cevap.startswith("```"):
                    ham_cevap = ham_cevap.split("```")[1]
                    if ham_cevap.startswith("json"):
                        ham_cevap = ham_cevap[4:]
                ham_cevap = ham_cevap.strip()
 
                try:
                    kartlar = json.loads(ham_cevap)
                    st.session_state["kartlar"] = kartlar
                    st.session_state["kart_index"] = 0
                    st.session_state["ters"] = False
                except:
                    st.error("Kartlar yuklenemedi, tekrar dene.")
 
        if "kartlar" in st.session_state and st.session_state["kartlar"]:
            kartlar = st.session_state["kartlar"]
            index = st.session_state["kart_index"]
            kart = kartlar[index]
 
            st.markdown(f"**Kart {index+1} / {len(kartlar)}**")
            st.markdown("---")
 
            if not st.session_state["ters"]:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:20px;padding:50px 40px;text-align:center;color:white;font-size:1.3rem;font-weight:600;box-shadow:0 10px 40px rgba(102,126,234,0.4);min-height:200px;display:flex;align-items:center;justify-content:center;margin:20px 0;">
                    {kart['on']}
                </div>
                <p style="text-align:center;color:#999;font-size:0.9rem;">Cevabi gormek icin Cevir butonuna bas</p>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#11998e,#38ef7d);border-radius:20px;padding:50px 40px;text-align:center;color:white;font-size:1.3rem;font-weight:600;box-shadow:0 10px 40px rgba(17,153,142,0.4);min-height:200px;display:flex;align-items:center;justify-content:center;margin:20px 0;">
                    {kart['arka']}
                </div>
                <p style="text-align:center;color:#999;font-size:0.9rem;">On yuze donmek icin Cevir butonuna bas</p>
                """, unsafe_allow_html=True)
 
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Onceki", key="onceki"):
                    if st.session_state["kart_index"] > 0:
                        st.session_state["kart_index"] -= 1
                        st.session_state["ters"] = False
                    st.rerun()
            with col2:
                if st.button("Cevir", key="cevir"):
                    st.session_state["ters"] = not st.session_state["ters"]
                    st.rerun()
            with col3:
                if st.button("Sonraki", key="sonraki"):
                    if st.session_state["kart_index"] < len(kartlar) - 1:
                        st.session_state["kart_index"] += 1
                        st.session_state["ters"] = False
                    st.rerun()
 
    with sekme4:
        st.subheader("PDF ile Sohbet")
        st.write("PDF icerigi hakkinda her seyi sorabilirsin.")
 
        if "sohbet_gecmisi" not in st.session_state:
            st.session_state["sohbet_gecmisi"] = []
 
        for mesaj in st.session_state["sohbet_gecmisi"]:
            if mesaj["role"] == "user":
                st.chat_message("user").write(mesaj["content"])
            else:
                st.chat_message("assistant").write(mesaj["content"])
 
        soru = st.chat_input("PDF hakkinda bir soru sor...")
 
        if soru:
            st.session_state["sohbet_gecmisi"].append({"role": "user", "content": soru})
            st.chat_message("user").write(soru)
 
            with st.spinner("Dusunuyor..."):
                mesajlar = [
                    {"role": "system", "content": f"Sen yardimci bir egitim asistanisin. Asagidaki PDF icerigi sana verildi. Sadece bu icerigi kullanarak Turkce cevap ver. Teknik terimleri orijinal dilde birak.\n\nPDF ICERIGI:\n{metin}"}
                ]
                mesajlar += st.session_state["sohbet_gecmisi"]
 
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=mesajlar
                )
                cevap = response.choices[0].message.content
                st.session_state["sohbet_gecmisi"].append({"role": "assistant", "content": cevap})
                st.chat_message("assistant").write(cevap)
 
    with sekme5:
        st.subheader("Akilli Analiz")
 
        col1, col2 = st.columns(2)
 
        with col1:
            st.markdown("#### 💪 Motivasyon Kocu")
            if st.button("Motivasyon Ver!", key="motivasyon_btn"):
                with st.spinner("Hazirlaniyor..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Sen enerjik bir calisma kocusu ve mentordasin. Kisa, etkili, samimi Turkce yaz."},
                            {"role": "user", "content": f"Ogrenci su konuyu calisiyor: {metin[:500]}. Ona 3-4 cumlelik motive edici mesaj yaz."}
                        ]
                    )
                    st.markdown(f"""
                    <div style="background:linear-gradient(135deg,#f093fb,#f5576c);border-radius:16px;padding:24px;color:white;font-size:1.1rem;line-height:1.6;box-shadow:0 8px 25px rgba(240,83,251,0.3);margin-top:16px;">
                        {response.choices[0].message.content}
                    </div>
                    """, unsafe_allow_html=True)
 
        with col2:
            st.markdown("#### 🎯 Zorluk Analizi")
            if st.button("Analiz Et", key="zorluk_btn"):
                with st.spinner("Analiz ediliyor..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Sen bir egitim uzmanisin. Turkce cevap ver."},
                            {"role": "user", "content": f"Su ders notunu analiz et:\n1. Zorluk seviyesi?\n2. On bilgiler?\n3. En zor kavramlar?\n4. Kac saatte ogrenilir?\n\n{metin}"}
                        ]
                    )
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.write(response.choices[0].message.content)
                    st.markdown('</div>', unsafe_allow_html=True)
 
        st.markdown("---")
 
        col3, col4 = st.columns(2)
 
        with col3:
            st.markdown("#### 🔮 Sinav Soru Tahmini")
            if st.button("Soru Tahmin Et", key="tahmin_btn"):
                with st.spinner("Tahminler yapiliyor..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Sen deneyimli bir hocasin. Turkce yaz. Teknik terimleri orijinal dilde birak."},
                            {"role": "user", "content": f"Bu ders notundan bir hoca sinav yapacak olsa hangi sorulari sorar? En muhtemel 5 sinav sorusunu yaz ve her birinin neden sorulabilecegini kisaca acikla:\n\n{metin}"}
                        ]
                    )
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.write(response.choices[0].message.content)
                    st.markdown('</div>', unsafe_allow_html=True)
 
        with col4:
            st.markdown("#### 🔑 Onemli Kavramlar")
            if st.button("Kavramlari Cikar", key="kavram_cikar_btn"):
                with st.spinner("Kavramlar cikariliyor..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Sen bir egitim uzmanisin. Sadece JSON listesi don. Baska hicbir sey yazma. Format: [\"kavram1\", \"kavram2\"]"},
                            {"role": "user", "content": f"Bu metindeki en onemli 15 anahtar kavrami listele:\n\n{metin}"}
                        ]
                    )
                    ham = response.choices[0].message.content.strip()
                    if ham.startswith("```"):
                        ham = ham.split("```")[1]
                        if ham.startswith("json"):
                            ham = ham[4:]
                    ham = ham.strip()
                    try:
                        kavramlar = json.loads(ham)
                        badges = "".join([f"""
                        <span style="display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:6px 14px;border-radius:20px;margin:4px;font-size:0.85rem;font-weight:500;">
                            {k}
                        </span>""" for k in kavramlar])
                        st.markdown(f'<div style="margin-top:16px;">{badges}</div>', unsafe_allow_html=True)
                    except:
                        st.error("Kavramlar yuklenemedi, tekrar dene.")
 
        st.markdown("---")
 
        col5, col6 = st.columns(2)
 
        with col5:
            st.markdown("#### 🧮 Formul Cikarici")
            if st.button("Formulleri Cikar", key="formul_btn"):
                with st.spinner("Formuller aranıyor..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Sen bir matematik ve fen bilimleri uzmanisin. Turkce aciklama yaz ama formulleri oldugu gibi birak."},
                            {"role": "user", "content": f"Bu metindeki tum formulleri, denklemleri ve matematiksel ifadeleri cikar. Her birinin ne oldugunu kisaca acikla. Eger formul yoksa 'Bu dokumanda formul bulunamadi' de:\n\n{metin}"}
                        ]
                    )
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.write(response.choices[0].message.content)
                    st.markdown('</div>', unsafe_allow_html=True)
 
        with col6:
            st.markdown("#### 🗺️ Kavram Haritasi")
            if st.button("Kavram Haritasi Olustur", key="kavram_btn"):
                with st.spinner("Kavramlar cikariliyor..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "Sen bir egitim uzmanisin. Sadece JSON formatinda cevap ver. Turkce ozel karakterleri kullanma, sadece ASCII karakterler kullan. Baska hicbir sey yazma."},
                            {"role": "user", "content": f"""Su metinden kavram haritasi olustur:
{{
  "ana_konu": "Ana konunun adi",
  "kavramlar": [
    {{
      "kavram": "Kavram adi",
      "aciklama": "Kisa aciklama",
      "alt_kavramlar": ["alt kavram 1", "alt kavram 2"]
    }}
  ]
}}
Metin: {metin}"""}
                        ]
                    )
                    ham = response.choices[0].message.content.strip()
                    if ham.startswith("```"):
                        ham = ham.split("```")[1]
                        if ham.startswith("json"):
                            ham = ham[4:]
                    ham = ham.strip()
                    try:
                        
                        st.write("Ham cevap:", ham)  # debug icin
                        harita = json.loads(ham.encode('utf-8').decode('utf-8'))
                        harita = json.loads(ham.encode('utf-8').decode('utf-8'))
                        st.markdown(f"""
                        <div style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:16px;padding:20px;color:white;text-align:center;font-size:1.3rem;font-weight:700;margin-bottom:20px;">
                            {harita['ana_konu']}
                        </div>
                        """, unsafe_allow_html=True)
                        cols = st.columns(len(harita['kavramlar']))
                        for idx, kavram in enumerate(harita['kavramlar']):
                            with cols[idx]:
                                alt_liste = "".join([f"<li style='margin:4px 0'>{a}</li>" for a in kavram['alt_kavramlar']])
                                st.markdown(f"""
                                <div style="background:white;border-radius:14px;padding:16px;box-shadow:0 4px 15px rgba(0,0,0,0.08);border-top:4px solid #667eea;">
                                    <div style="font-weight:700;color:#667eea;font-size:1rem;margin-bottom:8px">{kavram['kavram']}</div>
                                    <div style="font-size:0.85rem;color:#666;margin-bottom:12px">{kavram['aciklama']}</div>
                                    <ul style="font-size:0.8rem;color:#888;padding-left:16px;margin:0">{alt_liste}</ul>
                                </div>
                                """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Hata: {e}")
                        st.write("Ham cevap:", ham)
 
else:
    st.markdown("""
    <div style="text-align:center; padding:60px 20px; color:#999;">
        <div style="font-size:4rem;">📄</div>
        <h3 style="color:#ccc;">PDF yuklemek icin sol taraftaki alandan yukle</h3>
        <p>Ders notlarini yukle, yapay zeka ile calis</p>
    </div>
    """, unsafe_allow_html=True)
 