import requests
from bs4 import BeautifulSoup

URL = "https://www.biznesradar.pl/notowania/WODKAN#1d_lin_lin"

def get_company_profile(url: str) -> str:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Znajdujemy div z klasą "profileDesc"
    profile_div = soup.find("div", class_="profileDesc")
    if not profile_div:
        raise ValueError("Nie znaleziono sekcji 'Profil działalności' na stronie.")

    # Pobieramy tekst ze <span class="hidden">
    span = profile_div.find("span", class_="hidden")
    if not span:
        raise ValueError("Nie znaleziono elementu <span class='hidden'>.")

    description = span.get_text(strip=True)
    return description


if __name__ == "__main__":
    try:
        profile = get_company_profile(URL)
        print("=== Profil działalności spółki WODKAN ===")
        print(profile)

        # zapis do pliku
        with open("profil_dzialalnosci.txt", "w", encoding="utf-8") as f:
            f.write(profile)
        print("\nZapisano do pliku profil_dzialalnosci.txt")

    except Exception as e:
        print(f"Błąd: {e}")
