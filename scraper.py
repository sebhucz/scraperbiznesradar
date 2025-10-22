import requests
from bs4 import BeautifulSoup
from time import sleep

BASE_URL = "https://www.biznesradar.pl/notowania/{}#1d_lin_lin"
INPUT_FILE = "NCFOCUSNAZWY.txt"
OUTPUT_FILE = "profile_spolek.txt"

def get_company_profile(symbol: str) -> str:
    """Pobiera opis spółki z sekcji Profil działalności."""
    url = BASE_URL.format(symbol)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        return f"[{symbol}] Błąd: Nie udało się pobrać strony (HTTP {response.status_code})"

    soup = BeautifulSoup(response.text, "html.parser")
    profile_div = soup.find("div", class_="profileDesc")

    if not profile_div:
        return f"[{symbol}] Brak sekcji 'Profil działalności'."

    span = profile_div.find("span", class_="hidden")
    if not span:
        return f"[{symbol}] Brak opisu w sekcji 'Profil działalności'."

    description = span.get_text(strip=True)
    return description


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        companies = [line.strip() for line in f if line.strip()]

    results = []
    print(f"Znaleziono {len(companies)} spółek do przetworzenia...\n")

    for symbol in companies:
        print(f"Pobieram: {symbol}")
        try:
            profile = get_company_profile(symbol)
            results.append(f"=== {symbol} ===\n{profile}\n")
        except Exception as e:
            results.append(f"=== {symbol} ===\nBłąd: {e}\n")

        # Krótka pauza, żeby nie przeciążyć serwera
        sleep(1.5)

    # Zapis wyników
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n\n".join(results))

    print(f"\nZapisano wszystkie opisy do pliku {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
