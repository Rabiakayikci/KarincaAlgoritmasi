import matplotlib.pyplot as plt
import folium


def yol_gorsellestir(yol, koordinatlar):
    fig, ax = plt.subplots(figsize=(12, 10))

    for i in range(len(yol) - 1):
        idx1 = yol[i]
        idx2 = yol[i + 1]

        sehir1, (lat1, lon1) = koordinatlar[idx1]
        sehir2, (lat2, lon2) = koordinatlar[idx2]

        ax.plot([lon1, lon2], [lat1, lat2], 'k--', alpha=0.6)
        ax.text(lon1, lat1, sehir1, fontsize=9, color='darkblue')


    baslangic_idx = yol[0]
    _, (start_lat, start_lon) = koordinatlar[baslangic_idx]
    ax.scatter(start_lon, start_lat, c='red', s=100, label='Başlangıç')

    ax.set_title("SDÜ Kampüs Ring Seferi - En Kısa Rota")
    ax.set_xlabel("Boylam (Longitude)")
    ax.set_ylabel("Enlem (Latitude)")
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend()

    return fig


def yol_gorsellestir_folium(yol, koordinatlar):
    _, (lat0, lon0) = koordinatlar[yol[0]]

    harita = folium.Map(
        location=[lat0, lon0],
        zoom_start=16,
        tiles="OpenStreetMap"
    )


    for idx in yol:
        isim, (lat, lon) = koordinatlar[idx]
        folium.Marker(
            location=[lat, lon],
            popup=isim
        ).add_to(harita)


    rota = [(koordinatlar[i][1][0], koordinatlar[i][1][1]) for i in yol]

    folium.PolyLine(
        rota,
        color="blue",
        weight=4,
        opacity=0.8
    ).add_to(harita)

    return harita


def plot_convergence(best_distances):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(best_distances, marker='o')
    ax.set_title("Karınca Algoritması Performansı (Yakınsama Grafiği)")
    ax.set_xlabel("İterasyon (Tur Sayısı)")
    ax.set_ylabel("En Kısa Mesafe (km)")
    ax.grid(True)

    return fig
