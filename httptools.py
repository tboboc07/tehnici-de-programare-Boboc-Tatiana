"""Trusa de unelte HTTP: funcții care vorbesc cu httpbin.org."""

import requests

BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]

# Timeout-ul (în secunde) pentru funcțiile obișnuite și pentru raport
DEFAULT_TIMEOUT = 10
REPORT_TIMEOUT = 3


# ---------------------------------------------------------------------------
# Partea 1: parametri în URL
# ---------------------------------------------------------------------------
def search(params):
    """GET pe /get cu parametri în URL; returnează parametrii primiți de
    server."""
    r = requests.get(BASE + "/get", params=params, timeout=DEFAULT_TIMEOUT)
    return r.json()["args"]


def search_url(params):
    """Returnează adresa completă construită de requests, cu tot cu
    parametri."""
    r = requests.get(BASE + "/get", params=params, timeout=DEFAULT_TIMEOUT)
    return r.url


# ---------------------------------------------------------------------------
# Partea 2: anteturi
# ---------------------------------------------------------------------------
def fetch_with_agent(agent):
    """GET pe /headers cu User-Agent=agent; returnează User-Agent-ul văzut de
    server."""
    r = requests.get(
        BASE + "/headers",
        headers={"User-Agent": agent},
        timeout=DEFAULT_TIMEOUT,
    )
    return r.json()["headers"]["User-Agent"]


def default_agent():
    """Returnează User-Agent-ul trimis de requests când nu setezi nimic."""
    r = requests.get(BASE + "/headers", timeout=DEFAULT_TIMEOUT)
    return r.json()["headers"]["User-Agent"]


# ---------------------------------------------------------------------------
# Partea 3: trimiterea datelor
# ---------------------------------------------------------------------------
def post_json(data):
    """POST cu datele ca JSON pe /post; returnează JSON-ul primit de
    server."""
    r = requests.post(BASE + "/post", json=data, timeout=DEFAULT_TIMEOUT)
    return r.json()["json"]


def post_form(data):
    """POST cu datele ca formular pe /post; returnează formularul primit de
    server."""
    r = requests.post(BASE + "/post", data=data, timeout=DEFAULT_TIMEOUT)
    return r.json()["form"]


# ---------------------------------------------------------------------------
# Partea 4: coduri de stare
# ---------------------------------------------------------------------------
def describe_status(code):
    """GET pe /status/<code>; returnează 'succes', 'eroare client' sau
    'eroare server'."""
    try:
        r = requests.get(f"{BASE}/status/{code}", timeout=DEFAULT_TIMEOUT)
    except requests.RequestException:
        return "eroare de conexiune"  # nu ne oprim cu eroare

    if 200 <= r.status_code < 300:
        return "succes"
    if 400 <= r.status_code < 500:
        return "eroare client"
    if 500 <= r.status_code < 600:
        return "eroare server"
    return "alt cod"  # de exemplu 1xx sau 3xx


def is_ok(code):
    """GET pe /status/<code>; returnează True dacă cererea a reușit, altfel
    False."""
    try:
        r = requests.get(f"{BASE}/status/{code}", timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()  # ridică HTTPError pentru 4xx și 5xx
    except requests.RequestException:  # prinde și HTTPError, și erorile de rețea
        return False
    return True


# ---------------------------------------------------------------------------
# Partea 5: redirecționări
# ---------------------------------------------------------------------------
def count_redirects(n):
    """GET pe /redirect/<n>; returnează câte redirecționări au fost
    urmate."""
    r = requests.get(f"{BASE}/redirect/{n}", timeout=DEFAULT_TIMEOUT)
    return len(r.history)  # câte un răspuns pentru fiecare redirecționare


def final_url(n):
    """GET pe /redirect/<n>; returnează adresa la care ai ajuns."""
    r = requests.get(f"{BASE}/redirect/{n}", timeout=DEFAULT_TIMEOUT)
    return r.url


def first_hop(n):
    """GET pe /redirect/<n> FĂRĂ a urma redirecționarea; returnează antetul
    Location."""
    r = requests.get(
        f"{BASE}/redirect/{n}",
        allow_redirects=False,
        timeout=DEFAULT_TIMEOUT,
    )
    return r.headers.get("Location")


# ---------------------------------------------------------------------------
# Partea 6: sesiuni și cookie-uri
# ---------------------------------------------------------------------------
def cookie_demo(name, value):
    """Setează un cookie, apoi citește cookie-urile înapoi folosind O SINGURĂ
    sesiune."""
    with requests.Session() as s:
        # params= se ocupă de codificarea numelui și a valorii
        s.get(BASE + "/cookies/set", params={name: value},
              timeout=DEFAULT_TIMEOUT)
        r = s.get(BASE + "/cookies", timeout=DEFAULT_TIMEOUT)
        return r.json()["cookies"]


def no_session_demo(name, value):
    """Fă același lucru cu apeluri simple requests.get; returnează cookieurile
    văzute de server."""
    # Fiecare apel simplu pornește de la zero, deci cookie-ul se pierde
    requests.get(BASE + "/cookies/set", params={name: value},
                 timeout=DEFAULT_TIMEOUT)
    r = requests.get(BASE + "/cookies", timeout=DEFAULT_TIMEOUT)
    return r.json()["cookies"]  # va fi {}


# ---------------------------------------------------------------------------
# Partea 7: raportul final
# ---------------------------------------------------------------------------
def report(path):
    """Returnează un dicționar care descrie pagina de la BASE + path."""
    try:
        r = requests.get(BASE + path, timeout=REPORT_TIMEOUT)
    except requests.Timeout:
        return {"status": None, "error": "timeout"}
    except requests.ConnectionError:
        return {"status": None, "error": "fără conexiune"}
    except requests.RequestException as e:
        return {"status": None, "error": str(e)[:80]}

    return {
        "status": r.status_code,
        "final_url": r.url,
        "redirects": len(r.history),
        "seconds": round(r.elapsed.total_seconds(), 2),
        "content_type": r.headers.get("Content-Type"),
    }


def main():
    # 1. Apelăm report pentru fiecare adresă și păstrăm rezultatele
    results = []
    for path in PATHS:
        info = report(path)
        info["path"] = path  # adăugăm adresa, ca să o putem afișa
        results.append(info)

    # 2. Doar paginile cu status 200, cea mai lentă prima
    ok_pages = [info for info in results if info["status"] == 200]
    ok_pages.sort(key=lambda info: info["seconds"], reverse=True)

    for info in ok_pages:
        print(f"{info['path']} -> {info['status']}, {info['seconds']} secunde")

    # 3. Rezumatul
    failed = len(results) - len(ok_pages)
    print(f"Reușite: {len(ok_pages)} | Eșuate: {failed}")


# ---------------------------------------------------------------------------
# Bonus: autentificare
# ---------------------------------------------------------------------------
def check_login(user, password):
    """Returnează True dacă serverul acceptă datele de autentificare, altfel
    False."""
    try:
        # Trimitem datele ca octeți UTF-8: implicit requests folosește latin-1
        # și ar da UnicodeEncodeError la caractere precum "ș"
        r = requests.get(
            BASE + "/basic-auth/admin/secret",
            auth=(user.encode("utf-8"), password.encode("utf-8")),
            timeout=DEFAULT_TIMEOUT,
        )
    except requests.RequestException:
        return False
    return r.status_code == 200  # 401 înseamnă date greșite


if __name__ == "__main__":
    main()
