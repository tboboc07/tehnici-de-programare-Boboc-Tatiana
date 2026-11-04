# B1. Magic bytes: tipul real, nu extensia
def tip_real(cale):
    # Deschidem fișierul în mod binar și citim primii 8 octeți
    cap = open(cale, "rb").read(8)

    # Verificăm semnăturile (Magic Bytes)
    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"

    # Dacă nu se potrivește nicio semnătură cunoscută, returnăm reprezentarea hex
    return cap.hex()

# Rulăm funcția pe fișierul din probe/
print(tip_real("probe/foto.jpg"))
