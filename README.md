# 🎬 Movie Recommender System – MLOps Project
# **1. Entraînement du modèle (Notebook)**

Dans `notebooks/training.ipynb` :

* Chargement du dataset MovieLens 100K
* Nettoyage et preprocessing
* Construction d’une matrice user-item
* Modèle basé sur **SVD de Scikit-learn**
* Évaluation (RMSE)
* Export du modèle :

```
joblib.dump(model, "../models/recommender.joblib")
```

---

# **2. API FastAPI**

L’API expose l’endpoint :

```
POST /recommend
```
Démarrage local :

```
uvicorn src.api.main:app --reload
```

---

# **3. Interface Streamlit**

L’interface appelle l’API FastAPI déployée sur EC2.

```
streamlit run streamlit_app/app.py
```

Fonctionnalités :

* Saisie `user_id`
* Appel API via `requests`
* Affichage des recommandations

---

# **4. Conteneurisation Docker**

### API FastAPI

```
docker build -t movie-recommender .
docker run -p 8000:8000 movie-recommender
```

### Streamlit

```
docker build -f Dockerfile.streamlit -t streamlit-ui .
docker run -p 8501:8501 streamlit-ui
```

---

# **5. Déploiement AWS ECR**

Login :

```
aws ecr get-login-password --region eu-west-3 \
| docker login --username AWS --password-stdin <ID>.dkr.ecr.eu-west-3.amazonaws.com
```

Push images :

```
docker tag movie-recommender:latest <ID>.dkr.ecr.eu-west-3.amazonaws.com/movie-recommender
docker push <ID>.dkr.ecr.eu-west-3.amazonaws.com/movie-recommender
```

---

# **6. Déploiement AWS EC2**

Instance EC2 :

* Amazon Linux 2023
* t2.micro
* Ports ouverts :

  * `8000` (API)
  * `8501` (Streamlit)
  * `22` (SSH)

SSH :

```
ssh -i movie-key.pem ec2-user@<IP_PUBLIC>
```

Sur EC2 :

```
docker pull <ID>.dkr.ecr.eu-west-3.amazonaws.com/movie-recommender
docker pull <ID>.dkr.ecr.eu-west-3.amazonaws.com/streamlit-ui
```

Lancement :

```
docker run -d -p 8000:8000 movie-recommender
docker run -d -p 8501:8501 streamlit-ui
```

Accès navigateur :

* API : **http://13.38.11.164:8000/docs**
* UI : **http://13.38.11.164:8501**

---

# **7. CI/CD GitHub Actions (ECR + EC2)**

Ajout des secrets GitHub :

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_REGION`
* `ECR_REPO`
* `EC2_HOST`
* `EC2_USER`
* `EC2_KEY` (contenu du .pem encodé)

Pipeline `deploy.yml` :

* Build Docker
* Push vers ECR
* Connexion SSH à EC2
* Pull dernière image
* Restart containers

---

# **8. Exécution locale complète**

```
docker compose up --build
```

—→ API **[http://localhost:8000/docs](http://localhost:8000/docs)**
—→ UI **[http://localhost:8501](http://localhost:8501)**

---

# **9. Fonctionnalités du système**

* Recommandation personnalisée
* Interface intuitive
* Déploiement cloud scalable
* Versioning & CI/CD
* Architecture propre

---

# Membres

**Hiba Hamid**
**Ayoub Bellouch**
**Khaoula Mafkoud**
**Berkani Mohammed Adam**

---

