import re
import io
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS


def tip_real(cale):
    with open(cale, "rb") as f:
        cap = f.read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()


def strings(cale, minim=4):
    date = open(cale, "rb").read()
    return [m.decode() for m in re.findall(rb"[ -~]{%d,}" % minim, date)]

def in_zecimal(dms, emisfera):
    g, m, s = (float(x) for x in dms)
    val = g + m / 60 + s / 3600
    return -val if emisfera in ("S", "W") else val


def exif_complet(cale):
    exif = Image.open(cale).getexif()
    return {TAGS.get(k, k): v for k, v in exif.items()}


def gps(cale):
    g = Image.open(cale).getexif().get_ifd(0x8825)   # blocul GPS (tag 34853)
    if not g:
        return None
    return in_zecimal(g[2], g[1]), in_zecimal(g[4], g[3])


def carving(cale, iesire="gasit.zip"):
    date = open(cale, "rb").read()
    i = date.find(b"PK\x03\x04")
    if i == -1:
        return None
    open(iesire, "wb").write(date[i:])
    with zipfile.ZipFile(io.BytesIO(date[i:])) as z:
        continut = {n: z.read(n).decode() for n in z.namelist()}
    return i, continut

if __name__ == "__main__":
    for f in ("probe/foto.jpg", "probe/ascuns.png", "probe/mesaj.txt"):
        print("B1", f, "->", tip_real(f))
    print("B2", strings("probe/ascuns.png"))
    print("B3 EXIF:", exif_complet("probe/foto.jpg"))
    lat, lon = gps("probe/foto.jpg")
    print(f"B3 GPS: {lat:.5f}, {lon:.5f}")
    print("B4 carving:", carving("probe/ascuns.png"))
