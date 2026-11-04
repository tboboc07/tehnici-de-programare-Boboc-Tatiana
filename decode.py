s = "Salut"
b = s.encode()            # bytes
print(b, b[0])            # b"Salut" 83
# TODO: tipareste b.hex() si refa bytes din hex
#       cu bytes.fromhex(...)

import argparse
import json
import os

def desfa(date_intrare):
    # Funcția ta existentă care decodifică/analizează datele
    # Exemplu de bază conform testului:
    # return "base64", b"Salut"
    pass

def main():
    p = argparse.ArgumentParser()
    p.add_argument("intrare", help="sir sau cale")
    p.add_argument("--fisier", action="store_true", help="trateaza intrarea ca o cale catre un fisier")
    a = p.parse_args()

    # Citire date din fișier sau tratare ca șir de caractere
    if a.fisier:
        with open(a.intrare, "rb") as f:
            date = f.read()
    else:
        date = a.intrare.encode("utf-8")

    # Apelare funcție de decodificare
    strat, rezultat = desfa(date)

    # Pregătire date pentru JSON
    # Se convertește rezultatul în șir (dacă este bytes)
    rezultat_str = rezultat.decode("utf-8", errors="ignore") if isinstance(rezultat, bytes) else str(rezultat)

    date_salvare = {
        "strat": strat,
        "rezultat": rezultat_str
    }

    # Creare director și salvare în arsenal/forensics/fisa.json
    cale_iesire = os.path.join("arsenal", "forensics", "fisa.json")
    os.makedirs(os.path.dirname(cale_iesire), exist_ok=True)

    with open(cale_iesire, "w", encoding="utf-8") as f:
        json.dump(date_salvare, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()
