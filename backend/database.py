from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, ScrapeSession, JobSaved
from datetime import datetime
import os
from typing import List, Dict

# ---------------- Database Setup ----------------
DB_URL = os.getenv("DB_URL", "sqlite:///./jobs.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    """Initialise la base de données et crée toutes les tables."""
    Base.metadata.create_all(bind=engine)

# ---------------- Scrape Sessions ----------------
def create_scrape_session(db: Session, date: str, offers: List[Dict]):
    """Créer une nouvelle session de scraping avec ses offres."""
    session = ScrapeSession(
        date=date,
        created_at=datetime.utcnow(),
        total_offers=len(offers),
        offers=offers
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_scrape_sessions(db: Session):
    """Retourne toutes les sessions de scraping."""
    return db.query(ScrapeSession).order_by(ScrapeSession.date.desc()).all()

def get_offers_by_session(db: Session, date: str):
    """Retourne toutes les offres d’une session donnée."""
    session = db.query(ScrapeSession).filter(ScrapeSession.date == date).first()
    return session.offers if session else []

def clear_scraped_jobs(db: Session):
    """Supprime toutes les sessions et offres scrappées."""
    deleted = db.query(ScrapeSession).delete()
    db.commit()
    return deleted

# ---------------- Jobs Sauvegardés ----------------
def save_job_saved(db: Session, job: Dict):
    """
    Sauvegarde ou met à jour une offre dans les jobs sauvegardés.
    Limite à 1000 jobs : supprime les plus anciens si nécessaire.
    """
    allowed_fields = {"Titre", "Entreprise", "Localisation", "Lien", "Publié"}
    filtered_job = {k: v for k, v in job.items() if k in allowed_fields}

    # Vérification existence par Titre + Localisation + Entreprise
    existing = db.query(JobSaved).filter(
        JobSaved.Titre == filtered_job.get("Titre"),
        JobSaved.Localisation == filtered_job.get("Localisation"),
        JobSaved.Entreprise == filtered_job.get("Entreprise")
    ).first()

    if existing:
        # Mettre à jour si déjà existant
        existing.Lien = filtered_job.get("Lien", existing.Lien)
        existing.Publié = filtered_job.get("Publié", existing.Publié)
        existing.date_enreg = datetime.utcnow()
        db.commit()
        return existing
    else:
        # Avant insertion, vérifier si plus de 1000 jobs
        total_jobs = db.query(JobSaved).count()
        if total_jobs >= 1000:
            # Supprimer les plus anciens jobs pour faire de la place
            to_delete = db.query(JobSaved).order_by(JobSaved.date_enreg.asc()).limit(total_jobs - 100).all()
            for job_old in to_delete:
                db.delete(job_old)
            db.commit()

        # Ajouter le nouveau job
        new_job = JobSaved(**filtered_job, date_enreg=datetime.utcnow())
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return new_job


def get_jobs_saved(db: Session):
    """Retourne tous les jobs sauvegardés."""
    return db.query(JobSaved).order_by(JobSaved.date_enreg.desc()).all()

def clear_jobs_saved(db: Session):
    """Supprime tous les jobs sauvegardés."""
    deleted = db.query(JobSaved).delete()
    db.commit()
    return deleted
