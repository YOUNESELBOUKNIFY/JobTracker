Parfait ! Pour ton projet complet qui contient **l’accueil, le scraper LinkedIn et le scraper Stagiaires**, voici un exemple détaillé de **README.md** adapté :

````markdown
# Job Scraper App

Une application web pour **scraper automatiquement les offres d'emploi et de stage** depuis LinkedIn et Stagiaires.ma, et les gérer en temps réel.

---

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Usage](#usage)
- [Structure du projet](#structure-du-projet)

---

## Fonctionnalités

- Scraper les offres depuis **LinkedIn** et **Stagiaires.ma**.  
- Affichage des **nouvelles offres** et des **offres déjà enregistrées**.  
- Gestion des statuts des offres : `À postuler`, `Postulé`, `Entretien`, `Refusé`.  
- Tri des offres par date de publication (clic sur "Publié").  
- Sauvegarde des offres et statuts dans un fichier CSV (`jobs_status.csv`).  
- Interface responsive et moderne avec **Tailwind CSS**.  
- Utilisation de `sessionStorage` pour conserver les nouvelles offres entre les rechargements.  

---

## Technologies utilisées

- Frontend : HTML + Tailwind CSS + JavaScript Vanilla  
- Backend : [FastAPI](https://fastapi.tiangolo.com/) ou équivalent Python/Node.js  
- Scraping : [Requests](https://docs.python-requests.org/) + [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)  
- Stockage : CSV (`jobs_status.csv`)  

---

## Installation

1. **Cloner le projet**

```bash
git clone https://github.com/votre-utilisateur/job-scraper-app.git
cd job-scraper-app
````

2. **Créer un environnement virtuel**

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Lancer le serveur**

```bash
uvicorn main:app --reload
```

---

## Usage

1. Ouvrir le navigateur et aller à :
   `http://127.0.0.1:8000/static/index.html`

2. Sur la page d’accueil, choisir le scraper :

   * **LinkedIn**
   * **Stagiaires.ma**

3. Cliquer sur **Scraper** pour récupérer les offres.

4. Consulter les **nouvelles offres** et les **offres enregistrées**.

5. Modifier le **statut** d’une offre et cliquer sur **Enregistrer**.

6. Trier les nouvelles offres par date en cliquant sur **Publié**.

---

## Structure du projet

```
job-scraper-app/
│
├─ main.py                  # Serveur FastAPI ou Node.js
├─ requirements.txt         # Dépendances Python
├─ jobs_status.csv          # Statuts sauvegardés
├─ static/
│  ├─ index.html            # Page d’accueil
│  ├─ linkedin.html         # Scraper LinkedIn
│  └─ stagiaires.html       # Scraper Stagiaires.ma
├─ utils/
│  ├─ linkedin_parser.py    # Scraper LinkedIn
│  └─ stagiaires_parser.py  # Scraper Stagiaires.ma
└─ README.md
```

---




---

## Licence

Ce projet est sous licence MIT.

```

---

```
