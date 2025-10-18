# utils/run_spider.py
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

def fetch_and_save_stagiaires(base_url: str, max_jobs: int = 200, pause: float = 2.0):
    """
    Récupère toutes les offres de stagiaires.ma en suivant la pagination, parse les infos et retourne un DataFrame.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    all_jobs = []
    page = 1

    while True:
        url = f"{base_url}?page={page}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"⚠️ Erreur {resp.status_code} sur la page {page}")
            break

        soup = BeautifulSoup(resp.text, 'html.parser')
        offres = soup.select("div.section_cards_offres")
        if not offres:
            break

        for offre in offres:
            all_jobs.append({
                "Titre": offre.select_one("h3.title_card_offre_n").get_text(strip=True) if offre.select_one("h3.title_card_offre_n") else None,
                "Entreprise": offre.select_one("span.societe_name").get_text(strip=True) if offre.select_one("span.societe_name") else None,
                "Localisation": offre.select_one('span[data-tooltip="Ville"]').get_text(strip=True) if offre.select_one('span[data-tooltip="Ville"]') else None,
                "Publié": offre.select_one('span[data-tooltip="Date de publication"]').get_text(strip=True) if offre.select_one('span[data-tooltip="Date de publication"]') else None,
                "Lien": base_url + offre.select_one("a")["href"] if offre.select_one("a") else None,
            })

        page += 1
        if len(all_jobs) >= max_jobs:
            break

        time.sleep(pause)

    df = pd.DataFrame(all_jobs).head(max_jobs)
    return df
