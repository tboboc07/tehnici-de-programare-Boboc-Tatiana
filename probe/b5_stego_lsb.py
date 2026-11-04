from PIL import Image

# 1. Deschidem imaginea gazdă și o convertim la RGB
img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())

# 2. Definim mesajul și îl convertim într-un șir de biți
mesaj = b"FLAG{ascuns_in_pixeli}"
biti = "".join(f"{x:08b}" for x in mesaj)

# 3. Aplatizăm lista de pixeli într-o listă de canale de culoare individuale (valori întregi)
canale = []
for p in px:
    canale.extend(p)

# 4. Înlocuim LSB-ul fiecărui canal cu bitul din mesaj
for idx, bit in enumerate(biti):
    canale[idx] = (canale[idx] & ~1) | int(bit)

# 5. Reconstruim tuplurile RGB
px_nou = []
for i in range(0, len(canale), 3):
    px_nou.append((canale[i], canale[i+1], canale[i+2]))

# 6. Salvăm imaginea ca PNG
img.putdata(px_nou)
img.save("stego.png")
print("Mesajul a fost ascuns cu succes în 'stego.png'!")
