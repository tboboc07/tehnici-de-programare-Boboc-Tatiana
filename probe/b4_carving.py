import zipfile
import os

# 1. Citim datele binare ale imaginii
date = open("probe/ascuns.png", "rb").read()

# 2. Căutăm poziția semnăturii arhivei ZIP (PK\x03\x04)
i = date.find(b"PK\x03\x04")

if i != -1:
    # Salvăm datele începând de la indexul 'i' până la final într-un fișier nou .zip
    cale_zip = "gasit.zip"
    open(cale_zip, "wb").write(date[i:])
    print(f"Arhiva extrasă cu succes de la octetul {i}")

    # 3. Dezarhivăm și vedem ce era înăuntru
    director_extragere = "extrase"
    os.makedirs(director_extragere, exist_ok=True)

    with zipfile.ZipFile(cale_zip, "r") as zip_ref:
        zip_ref.extractall(director_extragere)
        fisiere_continute = zip_ref.namelist()
        print(f"Fișiere găsite în arhivă: {fisiere_continute}")

    # Afișăm conținutul fișierelor text extrase (dacă există)
    for nume_fisier in fisiere_continute:
        cale_completa = os.path.join(director_extragere, nume_fisier)
        if os.path.isfile(cale_completa):
            try:
                with open(cale_completa, "r", encoding="utf-8") as f:
                    print(f"\n--- Conținut {nume_fisier} ---")
                    print(f.read())
            except Exception:
                pass
else:
    print("Nu s-a găsit nicio semnătură ZIP în fișier.")
