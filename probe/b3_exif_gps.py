from PIL import Image
from PIL.ExifTags import TAGS

# Deschidem imaginea și citim metadatele EXIF
exif = Image.open("probe/foto.jpg")._getexif() or {}

print("--- Toate metadatele EXIF găsite ---")
for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)

# TODO: ia blocul GPS (tag 34853 / 0x8825) și tipărește latitudinea și longitudinea
gps_info = exif.get(34853, {})

def dms_to_decimal(dms, ref):
    """
    Convertește un tuplu (Grade, Minute, Secunde) în grade zecimale.
    Formula: Grade + (Minute / 60) + (Secunde / 3600)
    Dacă emisfera este 'S' sau 'W', valoarea devine negativă.
    """
    deg = float(dms[0])
    min_ = float(dms[1])
    sec = float(dms[2])

    dec = deg + (min_ / 60.0) + (sec / 3600.0)
    if ref in ['S', 'W']:
        dec = -dec
    return dec

if gps_info:
    print("\n--- Coordonate GPS ---")

    # 1: Ref Latitudine (N/S), 2: Latitudine (deg, min, sec)
    lat_ref = gps_info.get(1, 'N')
    lat_dms = gps_info.get(2)

    # 3: Ref Longitudine (E/W), 4: Longitudine (deg, min, sec)
    lon_ref = gps_info.get(3, 'E')
    lon_dms = gps_info.get(4)

    if lat_dms and lon_dms:
        lat_dec = dms_to_decimal(lat_dms, lat_ref)
        lon_dec = dms_to_decimal(lon_dms, lon_ref)

        print(f"Latitudine zecimală:  {lat_dec:.6f}")
        print(f"Longitudine zecimală: {lon_dec:.6f}")
        print(f"Coordonate Google Maps: {lat_dec:.6f}, {lon_dec:.6f}")
    else:
        print("Datele GPS incomplete în tag-ul 34853.")
else:
    print("Nu s-au găsit date GPS (tag 34853).")
