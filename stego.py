from PIL import Image


def ascunde(cale_gazda, mesaj, iesire="stego.png"):
    img = Image.open(cale_gazda).convert("RGB")
    canale = list(img.tobytes())                       # R,G,B,R,G,B...
    biti = "".join(f"{x:08b}" for x in mesaj + b"\x00")  # \x00 = sfarsit
    if len(biti) > len(canale):
        raise ValueError("mesaj prea lung pentru poza")
    for i, bit in enumerate(biti):
        canale[i] = (canale[i] & ~1) | int(bit)
    Image.frombytes("RGB", img.size, bytes(canale)).save(iesire)   # PNG, fara pierderi


def dezvaluie(cale):
    date = Image.open(cale).convert("RGB").tobytes()
    biti = "".join(str(c & 1) for c in date)
    out = bytearray()
    for i in range(0, len(biti) - 7, 8):
        o = int(biti[i:i + 8], 2)
        if o == 0:
            break
        out.append(o)
    return bytes(out).decode("utf-8", "replace")


if __name__ == "__main__":
    ascunde("probe/foto.jpg", b"FLAG{ascuns_in_pixeli}", "stego.png")
    print("dezvaluit:", dezvaluie("stego.png"))
