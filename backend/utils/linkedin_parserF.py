import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

def fetch_and_save_jobs(base_url: str, output_file: str = "linkedin_jobs.csv", max_jobs: int = 200, pause: float = 2.0):
    """
    Récupère toutes les offres LinkedIn en suivant la pagination, parse les infos et exporte en CSV.
    
    Args:
        base_url (str): URL de recherche LinkedIn sans paramètre start
        output_file (str): Nom du fichier CSV à créer
        max_jobs (int): Nombre maximum d'offres à récupérer
        pause (float): Temps de pause entre les requêtes pour éviter le blocage
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    all_jobs = []
    start = 0
    page_size = 25  # LinkedIn affiche 25 jobs par page

    while True:
        url = f"{base_url}&start={start}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"⚠️ Erreur {resp.status_code} sur la page start={start}")
            break

        soup = BeautifulSoup(resp.text, 'html.parser')
        job_list_ul = soup.find_all('ul', class_='jobs-search__results-list')

        if not job_list_ul:
            print(" Plus d'offres à récupérer.")
            break

        for ul in job_list_ul:
            li_items = ul.find_all('li')
            for li in li_items:
                all_jobs.append({
                    "Titre": li.find('h3', class_='base-search-card__title').get_text(strip=True) if li.find('h3', class_='base-search-card__title') else None,
                    "Entreprise": li.find('h4', class_='base-search-card__subtitle').get_text(strip=True) if li.find('h4', class_='base-search-card__subtitle') else None,
                    "Localisation": li.find('span', class_='job-search-card__location').get_text(strip=True) if li.find('span', class_='job-search-card__location') else None,
                    "Lien": li.find('a', class_='base-card__full-link')['href'] if li.find('a', class_='base-card__full-link') else None,
                    "Publié": li.find('time', class_='job-search-card__listdate').get_text(strip=True) if li.find('time', class_='job-search-card__listdate') else None,
                    "Recrutement": li.find('div', class_='job-posting-benefits').get_text(strip=True) if li.find('div', class_='job-posting-benefits') else None,
                })

        print(f" Page start={start} terminée. Total jobs récupérés : {len(all_jobs)}")

        start += page_size

        if len(all_jobs) >= max_jobs:
            print(f"⚠️ Limite max_jobs={max_jobs} atteinte.")
            break

        time.sleep(pause)  # pause pour réduire le risque de blocage

    # Exporter vers CSV
    df = pd.DataFrame(all_jobs)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Tous les jobs sauvegardés dans {output_file} ({len(df)} lignes)")
    return df
