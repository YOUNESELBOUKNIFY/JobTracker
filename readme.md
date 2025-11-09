# Job Scraper LinkedIn

Une application simple pour récupérer et gérer les offres d'emploi LinkedIn.

## Démo

https://drive.google.com/file/d/1B0YSg7hbFaXbK-bmbztNdY3cyZZp37dM/view?usp=sharing

##  Application
https://jobscraper.up.railway.app/
##  Installation

```bash
# Cloner le projet
git clone https://github.com/YOUNESELBOUKNIFY/JobScraper

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
uvicorn main:app --reload
```


##  Fonctionnalités

- ✅ Scraping automatique des offres LinkedIn
- ✅ Sauvegarde dans SQLite
- ✅ Interface web simple
- ✅ Suppression des doublons
- ✅ Scraping automatique toutes les 4h

## API Endpoints

- `GET /scrape/linkedin` - Lancer le scraping
- `GET /jobs/saved` - Liste des offres
- `DELETE /jobs/saved/delete` - Supprimer une offre
- `GET /sessions` - Sessions de scraping

##  Structure

```
main.py          # Application FastAPI
database.py      # Gestion base de données
static/          # Fichiers HTML/CSS/JS
utils  # Script de scraping
```

