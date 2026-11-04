# B2. strings: textul citibil dintr-un binar
import re

# Deschidem fișierul în mod binar
date = open("probe/ascuns.png", "rb").read()

# Extrapolăm secvențele de cel puțin 4 caractere imprimabile ASCII (de la spațiu ' ' până la '~')
for m in re.findall(rb"[ -~]{4,}", date):
    text = m.decode("ascii", errors="ignore")
    print(text)

    # Căutăm un indiciu (o cale, un mesaj sau un nume de fișier)
    if "/" in text or ".txt" in text or "flag" in text.lower() or "secret" in text.lower():
        print(f"  -> [INDICIU POSIBIL]: {text}")
