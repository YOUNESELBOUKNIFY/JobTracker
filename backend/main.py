import asyncio
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os

from database import (
    SessionLocal, init_db, create_scrape_session, get_scrape_sessions,
    get_offers_by_session, get_jobs_saved, JobSaved
)
from utils.linkedin_parserF import fetch_and_save_jobs  # ton code scraping

app = FastAPI(title="Job Scraper SQLite", version="1.0")

static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Pages HTML ----------------
@app.get("/")
def root():
    return FileResponse(os.path.join(static_path, "index.html"))

@app.get("/linkedin")
def linkedin_redirect():
    return RedirectResponse(url="/static/linkedin.html")

# ---------------- Scraper LinkedIn manuel ----------------
def scrape_linkedin(db: Session):
    session_time = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    jobs = fetch_and_save_jobs(
        "https://www.linkedin.com/jobs/search/?currentJobId=4314731267&distance=25&f_E=1&f_JT=I&f_TPR=r86400&geoId=105015875&keywords=data%20scientist&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD",
        max_jobs=50
    )
    if not jobs:
        return {"message": "Aucun job récupéré"}

    # Filtrer les doublons déjà présents dans JobSaved (Titre + Localisation + Entreprise)
    filtered_jobs = []
    for job in jobs:
        exists = db.query(JobSaved).filter(
            JobSaved.Titre == job.get("Titre"),
            JobSaved.Localisation == job.get("Localisation"),
            JobSaved.Entreprise == job.get("Entreprise")
        ).first()
        if not exists:
            filtered_jobs.append(job)

    if not filtered_jobs:
        return {"message": "Aucun nouveau job à ajouter"}

    # Créer une session de scraping et enregistrer les offres dans la base
    try:
        create_scrape_session(db, session_time, filtered_jobs)
        # Ajouter dans JobSaved pour interface
        for job in filtered_jobs:
            js = JobSaved(
                Titre=job.get("Titre"),
                Entreprise=job.get("Entreprise"),
                Localisation=job.get("Localisation"),
                Lien=job.get("Lien"),
                Publié=job.get("Publié")
            )
            db.add(js)
        db.commit()
    except IntegrityError:
        db.rollback()
        return {"message": "Erreur lors de l'enregistrement en base"}

    return {"message": f"{len(filtered_jobs)} nouveaux jobs ajoutés à la session {session_time}"}

@app.get("/scrape/linkedin")
def scrape_linkedin_endpoint(db: Session = Depends(get_db)):
    return scrape_linkedin(db)

# ---------------- Jobs sauvegardés pour interface ----------------
@app.get("/jobs/saved")
def list_jobs_saved(db: Session = Depends(get_db)):
    jobs = get_jobs_saved(db)
    return JSONResponse([{
        "Titre": j.Titre,
        "Entreprise": j.Entreprise,
        "Localisation": j.Localisation,
        "Lien": j.Lien,
        "Publié": getattr(j, "Publié", None),
        "date_enreg": j.date_enreg.isoformat()
    } for j in jobs])

@app.delete("/jobs/saved/delete")
def delete_job_saved(Lien: str, db: Session = Depends(get_db)):
    job = db.query(JobSaved).filter(JobSaved.Lien == Lien).first()
    if not job:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    db.delete(job)
    db.commit()
    return JSONResponse({"message": "Offre supprimée"})

# ---------------- Sessions et offres ----------------
@app.get("/sessions")
def list_sessions(db: Session = Depends(get_db)):
    sessions = get_scrape_sessions(db)
    return JSONResponse([{
        "date": s.date,
        "total_offers": s.total_offers,
        "created_at": s.created_at.isoformat()
    } for s in sessions])

@app.get("/offers/{date}")
def get_offers(date: str, db: Session = Depends(get_db)):
    offers = get_offers_by_session(db, date)
    if not offers:
        raise HTTPException(status_code=404, detail="Aucune offre trouvée pour cette date")
    return JSONResponse(offers)

# ---------------- Scraping automatique toutes les 1h ----------------
async def periodic_scraping():
    await asyncio.sleep(5)  # petit délai au démarrage
    while True:
        print("⏳ Scraping automatique LinkedIn...")
        try:
            db = SessionLocal()
            scrape_linkedin(db)
        except Exception as e:
            print("Erreur lors du scraping automatique :", e)
        finally:
            db.close()
        await asyncio.sleep(3600)  # attendre 1h avant le prochain scraping

# ---------------- Startup ----------------
@app.on_event("startup")
async def on_startup():
    init_db()
    print("✅ Base SQLite prête")
    asyncio.create_task(periodic_scraping())
