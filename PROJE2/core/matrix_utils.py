import numpy as np
import googlemaps
from geopy.distance import geodesic
import time

def haversine_distance(coord1, coord2):
  
    if len(coord1) == 2 and isinstance(coord1[1], tuple):
        c1 = coord1[1]
    else:
        c1 = coord1
    if len(coord2) == 2 and isinstance(coord2[1], tuple):
        c2 = coord2[1]
    else:
        c2 = coord2
    return geodesic(c1, c2).km

def mesafe_matrisi_olustur(koordinatlar, api_key=None):
    
    n = len(koordinatlar)
    matris = np.zeros((n, n))
    sadece_koordinatlar = [k[1] for k in koordinatlar]

    if api_key:
        try:
            print(f"🌍 Google Maps API ile {n}x{n} matris parçalar halinde hesaplanıyor...")
            gmaps = googlemaps.Client(key=api_key)
            
          
            chunk_size = 5
            
            for i in range(0, n, chunk_size):
                for j in range(0, n, chunk_size):
                    origins_chunk = sadece_koordinatlar[i : i + chunk_size]
                    dests_chunk = sadece_koordinatlar[j : j + chunk_size]
                    
                    response = gmaps.distance_matrix(
                        origins=origins_chunk,
                        destinations=dests_chunk,
                        mode="driving"
                    )
                    
                    for r_idx, row in enumerate(response['rows']):
                        for e_idx, element in enumerate(row['elements']):
                            if element['status'] == 'OK':
                                dist_km = element['distance']['value'] / 1000.0
                                matris[i + r_idx][j + e_idx] = dist_km
                            else:
                                c1 = origins_chunk[r_idx]
                                c2 = dests_chunk[e_idx]
                                matris[i + r_idx][j + e_idx] = geodesic(c1, c2).km
            
            print("✅ Google Maps verileri başarıyla çekildi.")
            return matris

        except Exception as e:
            print(f"⚠️ Google API Hatası: {e}")
            print("🔄 Hata olduğu için Kuş Uçuşu (Haversine) moduna geçiliyor...")

    
    print("📏 Kuş uçuşu hesaplama yapılıyor...")
    for i in range(n):
        for j in range(n):
            if i != j:
                matris[i][j] = haversine_distance(koordinatlar[i], koordinatlar[j])
    
    return matris


def hesapla_cekicilik(mesafe_matrisi):
    
    with np.errstate(divide='ignore'):
        cekicilik = 1.0 / mesafe_matrisi
    
    
    cekicilik[mesafe_matrisi == 0] = 0
    return cekicilik