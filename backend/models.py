from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# ===============================
# Table des sessions de scraping
# ===============================
class ScrapeSession(Base):
    __tablename__ = "scrape_sessions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_offers = Column(Integer)
    offers = Column(JSON)  # Stocke les offres scrappées


# ===============================
# Table des offres sauvegardées
# ===============================
class JobSaved(Base):
    __tablename__ = "jobs_saved"

    id = Column(Integer, primary_key=True, index=True)
    Titre = Column(String)
    Entreprise = Column(String)
    Localisation = Column(String)
    Lien = Column(String, unique=True)
    Publié = Column(String)               # Ex: "il y a 3 jours"
    date_enreg = Column(DateTime, default=datetime.utcnow)
