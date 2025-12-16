import numpy as np

def haversine(koordinat1, koordinat2): #başlangıç noktası,bitiş noktası arası hesaplanmak istenilen yer
    
    R = 6371  # Dünya yarıçapı (km)
    lat1, lon1 = np.radians(koordinat1)
    lat2, lon2 = np.radians(koordinat2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c