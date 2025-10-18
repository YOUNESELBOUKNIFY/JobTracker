from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
from fastapi.responses import RedirectResponse
import csv
import pandas as pd

# Import des fonctions de scraping
from utils.linkedin_parserF import fetch_and_save_jobs
from utils.run_spider import fetch_and_save_stagiaires  # fonction qui retourne DataFrame

# Fichiers CSV pour les statuts
STATUS_CSV = "jobs_status.csv"
APPLIED_CSV = "jobs_status.csv"

# Création de l'application FastAPI
app = FastAPI(
    title="Job Scraper API",
    description="API pour scraper plusieurs sites d'offres d'emploi",
    version="1.0"
)

# Chemin vers le dossier static
static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

# -------------------------------
# Pages HTML
# -------------------------------

@app.get("/")
def root():
    index_path = os.path.join(static_path, "index.html")
    return FileResponse(index_path)




@app.get("/linkedin")
def linkedin_redirect():
    return RedirectResponse(url="/static/linkedin.html")

@app.get("/stagiaires")
def stagiaires_page():
    path = os.path.join(static_path, "stagiaires.html")
    return FileResponse(path)

# -------------------------------
# Endpoints API
# -------------------------------

@app.get("/scrape/linkedin")
def scrape_linkedin_jobs(
    url: str = Query(
        "https://fr.linkedin.com/jobs/search?keywords=Data&location=France",
        description="URL de recherche LinkedIn"
    ),
    max_jobs: int = Query(100, description="Nombre maximum de jobs à récupérer")
):
    try:
        df = fetch_and_save_jobs(url, max_jobs=max_jobs)
        return JSONResponse(content=df.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/scrape/stagiaires")
def scrape_stagiaires_jobs():
    try:
        BASE_URL = "https://www.stagiaires.ma/offres-de-stages-et-premier-emploi-maroc/?types_de_contrat=Stage"
        df = fetch_and_save_stagiaires(BASE_URL, max_jobs=100, pause=1.5)
        return JSONResponse(content=df.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/jobs/status/list")
def get_job_status_list():
    if not os.path.exists(STATUS_CSV):
        return JSONResponse(content={})
    with open(STATUS_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        status_dict = {row["Lien"]: row["Statut"] for row in reader if row.get("Lien")}
    return JSONResponse(content=status_dict)

@app.get("/jobs/applied/full")
def get_applied_jobs_full():
    if not os.path.exists(APPLIED_CSV):
        return JSONResponse(content=[])
    with open(APPLIED_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        applied_jobs = [row for row in reader]
    return JSONResponse(content=applied_jobs)

@app.post("/jobs/status")
async def save_job_status(job: dict):
    headers = ["Titre", "Entreprise", "Localisation", "Lien", "Publié", "Recrutement", "Statut"]

    existing_status = []
    if os.path.exists(STATUS_CSV):
        with open(STATUS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            existing_status = list(reader)

    # Vérifie si le job existe déjà
    updated = False
    for j in existing_status:
        if j.get("Lien") == job.get("Lien"):
            j.update(job)
            updated = True
            break

    if updated:
        with open(STATUS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(existing_status)
    else:
        with open(STATUS_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if os.stat(STATUS_CSV).st_size == 0:
                writer.writeheader()
            writer.writerow(job)

    return JSONResponse({"message": "Statut enregistré avec succès"})
