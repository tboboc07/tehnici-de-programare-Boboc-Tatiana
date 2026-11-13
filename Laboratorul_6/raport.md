# Lucrarea 6. Informații invizibile: forensics și steganografie

## Lucrarea A. Decoderul universal

- **Mesajul cu straturi (probe/mesaj.txt):** straturile base64 → base64 → hex; textul clar este `FLAG{straturi_de_encoding}`.
- **XOR (probe/xor.bin):** cheia găsită este 128 (0x80); textul: `Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}`.
- **Hash-uri (probe/hashuri.txt, md5):** parolele sparte prin dicționar: `password`, `dragon`, `qwerty`, `letmein`, `monkey`.

Comenzi folosite:

```
python arsenal/forensics/decode.py --fisier probe/mesaj.txt
python arsenal/forensics/decode.py --xor probe/xor.bin
python arsenal/forensics/decode.py --hash probe/wordlist.txt <hash>
python -m pytest teste
```

## Lucrarea B. Forensics pe fișiere

- **Tipul real al fișierelor (magic bytes):** `foto.jpg` este jpeg, `ascuns.png` este png, `mesaj.txt` nu are semnătură cunoscută (text).
- **Metadate EXIF:** Apple iPhone 13, data 2026:09:14 10:30:00.
- **GPS:** 47.01667 N, 28.85750 E (Chișinău); grade zecimale = grade + minute/60 + secunde/3600.
- **Arhiva ascunsă (file carving):** ZIP lipit la coada lui `ascuns.png`, începând de la octetul 782; conține `secret.txt` cu `FLAG{ascuns_prin_carving}`.
- **Mesajul LSB dezvăluit:** `FLAG{ascuns_in_pixeli}` (ascuns în `stego.png`).

Output:

```
B1 probe/foto.jpg -> jpeg
B1 probe/ascuns.png -> png
B3 GPS: 47.01667, 28.85750
B4 carving: (782, {'secret.txt': 'FLAG{ascuns_prin_carving}\n'})
dezvaluit: FLAG{ascuns_in_pixeli}
```
