import streamlit as st
import os
import toml
import folium
from streamlit_folium import st_folium
import googlemaps
import matplotlib.pyplot as plt


from data.coordinates import koordinatlar
from core.matrix_utils import mesafe_matrisi_olustur
from core.ant_algorithm import run_aco
from visual.plotting import plot_convergence 
from config import ACO_CONFIG


def decode_polyline(polyline_str):
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}
    while index < len(polyline_str):
        for unit in ['latitude', 'longitude']: 
            shift, result = 0, 0
            while True:
                byte = ord(polyline_str[index]) - 63
                index += 1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20: break
            if (result & 1): changes[unit] = ~(result >> 1)
            else: changes[unit] = (result >> 1)
        lat += changes['latitude']
        lng += changes['longitude']
        coordinates.append((lat / 100000.0, lng / 100000.0))
    return coordinates


def create_folium_map(yol, koordinatlar, api_key=None):
    
    baslangic_idx = yol[0]
    _, (lat0, lon0) = koordinatlar[baslangic_idx]

   
    m = folium.Map(location=[lat0, lon0], zoom_start=14, tiles="CartoDB positron")
    
   
    for idx in yol:
        isim, (lat, lon) = koordinatlar[idx]
        renk = 'red' if idx == baslangic_idx else 'blue'
        ikon = 'play' if idx == baslangic_idx else 'info-sign'
        folium.Marker(
            [lat, lon], popup=isim, tooltip=isim,
            icon=folium.Icon(color=renk, icon=ikon)
        ).add_to(m)

    
    if api_key:
        
        gmaps = googlemaps.Client(key=api_key)
        
       
        for i in range(len(yol) - 1):
            start_idx = yol[i]
            end_idx = yol[i+1]
            
            origin = koordinatlar[start_idx][1]      
            destination = koordinatlar[end_idx][1]   
            
            try:
                
                directions = gmaps.directions(origin, destination, mode="driving")
                
                if directions:
                    
                    encoded_poly = directions[0]['overview_polyline']['points']
                    path_points = decode_polyline(encoded_poly)
                    
                    
                    folium.PolyLine(
                        path_points, color="red", weight=4, opacity=0.8
                    ).add_to(m)
                else:
                    
                    folium.PolyLine([origin, destination], color="red", weight=4, opacity=0.8, dash_array='5, 10').add_to(m)
                    
            except Exception as e:
                
                print(f"Rota çizim hatası: {e}")
                folium.PolyLine([origin, destination], color="red", weight=4, opacity=0.8, dash_array='5, 10').add_to(m)

    else:
       
        rota_coords = [(koordinatlar[i][1]) for i in yol]
        folium.PolyLine(rota_coords, color="red", weight=4, opacity=0.8, dash_array='5, 10').add_to(m)

    return m


st.set_page_config(page_title="SDÜ Kampüs Ring", layout="wide")
st.title("🐜 SDÜ Kampüs Ring Seferi")
st.markdown("**Karınca Kolonisi Algoritması** ile en kısa rotayı buluyoruz.")


api_key = None
try:
    secrets_yolu = os.path.join(os.getcwd(), ".streamlit", "secrets.toml")
    if os.path.exists(secrets_yolu):
        config = toml.load(secrets_yolu)
        api_key = config.get("general", {}).get("GOOGLE_API_KEY")
except:
    pass

if api_key:
    st.success("✅ Google Maps Bağlantısı Aktif! (Gerçek yollar çiziliyor)")
else:
    st.warning("⚠️ Google Key yok, Düz çizgi (Kuş uçuşu) çizilecek.")


st.sidebar.header("⚙️ Ayarlar")
karinca_sayisi = st.sidebar.slider("Karınca Sayısı", 1, 50, ACO_CONFIG["karinca_sayisi"])
iterasyon_sayisi = st.sidebar.slider("İterasyon Sayısı", 1, 100, ACO_CONFIG["iterasyon_sayisi"])
alpha = st.sidebar.slider("Alpha (Feromon)", 0.1, 5.0, ACO_CONFIG["alpha"])
beta = st.sidebar.slider("Beta (Mesafe)", 0.1, 5.0, ACO_CONFIG["beta"])
buharlasma = st.sidebar.slider("Buharlaşma", 0.0, 1.0, ACO_CONFIG["buharlasma_orani"])
calistir = st.sidebar.button("🚀 Rotayı Hesapla", type="primary")

if "sonuc_var" not in st.session_state:
    st.session_state.sonuc_var = False

if calistir:
    with st.spinner("⏳ Rota optimize ediliyor..."):
        
        mesafe = mesafe_matrisi_olustur(koordinatlar, api_key=api_key)
        
        
        en_iyi_yol, en_iyi_mesafe, iterasyon_iyileri = run_aco(
            mesafe,
            karinca_sayisi=karinca_sayisi,
            iterasyon_sayisi=iterasyon_sayisi,
            alpha=alpha,
            beta=beta,
            buharlasma_orani=buharlasma,
            feromon_katkisi=1.0
        )
        
        st.session_state.en_iyi_yol = en_iyi_yol
        st.session_state.en_iyi_mesafe = en_iyi_mesafe
        st.session_state.iterasyon_iyileri = iterasyon_iyileri
        st.session_state.sonuc_var = True

if st.session_state.sonuc_var:
    st.divider()
    st.metric("🏁 Toplam Mesafe", f"{st.session_state.en_iyi_mesafe:.3f} km")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📉 Performans")
        fig_conv = plot_convergence(st.session_state.iterasyon_iyileri)
        st.pyplot(fig_conv)

    with col2:
        st.subheader("🗺️ Harita (Sokak Görünümü)")
       
        harita = create_folium_map(st.session_state.en_iyi_yol, koordinatlar, api_key=api_key)
        st_folium(harita, width=600, height=400, returned_objects=[])

elif not calistir:
    st.info("👈 Lütfen sol taraftaki 'Rotayı Hesapla' butonuna basın.")