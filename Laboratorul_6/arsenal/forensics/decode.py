# -*- coding: utf-8 -*-
"""Lucrarea A: decoder universal (A1-A7)."""
import argparse
import base64
import hashlib
import json
import os
import re
from urllib.parse import unquote

AICI = os.path.dirname(os.path.abspath(__file__))


# A1 - text vs octeti
def incalzire():
    s = "Salut"
    b = s.encode()
    print(b, b[0])                      # b'Salut' 83
    h = b.hex()
    print(h, bytes.fromhex(h))          # 53616c7574 b'Salut'


# A2 - recunoastere dupa forma (ordinea: url -> hex -> base64)
def ghici_strat(s):
    s = s.strip()
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if len(s) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", s):
        return "hex"
    if len(s) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"
    return "necunoscut"


# A3 - desfacere
def desfa(s):
    strat = ghici_strat(s)
    try:
        if strat == "base64":
            return strat, base64.b64decode(s)
        if strat == "hex":
            return strat, bytes.fromhex(s)
        if strat == "url":
            return strat, unquote(s).encode()
    except Exception:
        pass
    return "necunoscut", s.encode()


# A4 - straturi multiple
def citibil(b):
    return len(b) > 0 and all(32 <= c < 127 for c in b)


def desfa_lant(val, max_pasi=8):
    """Intoarce (lista_straturi, bytes_finali)."""
    straturi = []
    b = val.encode()
    for _ in range(max_pasi):
        strat, rez = desfa(val)
        if strat == "necunoscut":
            break
        straturi.append(strat)
        b = rez
        if not citibil(b):          # a iesit binar (ex. ceva criptat cu XOR)
            break
        val = b.decode()
    return straturi, b


# A5 - XOR cu cheie de un octet
def scor_text(t):
    """Cat de mult seamana cu text: litere + spatii (spatiile cantaresc dublu)."""
    litere = sum(ch.isalpha() for ch in t)
    spatii = t.count(" ")
    return (litere + 2 * spatii) / len(t)


def xor_brute(date):
    """Toate cheile pentru care rezultatul e imprimabil, cele mai 'text' primele.
    (Doar filtrul 'imprimabil' lasa si chei false, de aceea sortam dupa scor.)"""
    gasite = []
    for k in range(256):
        clar = bytes(x ^ k for x in date)
        if citibil(clar):
            gasite.append((k, clar.decode()))
    gasite.sort(key=lambda kt: scor_text(kt[1]), reverse=True)
    return gasite


# A6 - hash prin dictionar
ALGORITMI = {32: "md5", 40: "sha1", 64: "sha256"}


def sparge_hash(tinta, cale_wordlist):
    alg = ALGORITMI.get(len(tinta))
    if alg is None:
        return None, None
    with open(cale_wordlist, encoding="latin1") as f:
        for cuv in f:
            cuv = cuv.strip()
            if hashlib.new(alg, cuv.encode()).hexdigest() == tinta.lower():
                return alg, cuv
    return alg, None


# A7 - linia de comanda + fisa JSON
def main():
    p = argparse.ArgumentParser(description="Decoder universal")
    p.add_argument("intrare", help="sir sau cale")
    p.add_argument("--fisier", action="store_true", help="intrarea e o cale")
    p.add_argument("--xor", action="store_true", help="forta bruta XOR 1 octet (intrarea e fisier)")
    p.add_argument("--hash", metavar="WORDLIST", help="intrarea e un hash; cauta in wordlist")
    a = p.parse_args()

    if a.xor:
        date = open(a.intrare, "rb").read()
        gasite = xor_brute(date)
        fisa = {"strat": "xor", "rezultat": [{"cheie": k, "text": t} for k, t in gasite[:3]]}
    elif a.hash:
        alg, parola = sparge_hash(a.intrare.strip(), a.hash)
        fisa = {"strat": alg or "necunoscut", "rezultat": parola}
    else:
        if a.fisier:
            val = open(a.intrare, "rb").read().decode("utf-8", "replace").strip()
        else:
            val = a.intrare
        straturi, b = desfa_lant(val)
        fisa = {"strat": straturi,
                "rezultat": b.decode() if citibil(b) else b.hex()}

    print(json.dumps(fisa, indent=2, ensure_ascii=False))
    with open(os.path.join(AICI, "fisa.json"), "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
