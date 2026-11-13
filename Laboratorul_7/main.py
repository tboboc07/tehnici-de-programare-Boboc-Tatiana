"""Programul complet: folosește funcțiile din httptools."""

from httptools import PATHS, report


def main():
    # Apelăm report pentru fiecare adresă și păstrăm rezultatele
    results = []
    for path in PATHS:
        info = report(path)
        info["path"] = path  # adăugăm adresa, ca să o putem afișa
        results.append(info)

    # Doar paginile cu status 200, cea mai lentă prima
    ok_pages = [info for info in results if info["status"] == 200]
    ok_pages.sort(key=lambda info: info["seconds"], reverse=True)

    for info in ok_pages:
        print(f"{info['path']} -> {info['status']}, {info['seconds']} secunde")

    # Rezumatul
    failed = len(results) - len(ok_pages)
    print(f"Reușite: {len(ok_pages)} | Eșuate: {failed}")


if __name__ == "__main__":
    main()

