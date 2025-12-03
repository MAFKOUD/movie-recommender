# 🎬 **Movie Recommender System – MLOps Project**

Ce projet implémente un système complet de recommandation de films basé sur le dataset MovieLens.
Il comprend :

* un modèle de Machine Learning,
* une API FastAPI,
* une interface utilisateur Streamlit,
* une containerisation Docker,
* un déploiement sur AWS (ECR + EC2),
* et un pipeline CI/CD GitHub Actions.

---

## **1. Entraînement du modèle (Notebook)**

Dans `notebooks/training.ipynb` :

* Chargement du dataset **MovieLens 100K**
* Nettoyage et préprocessing
* Construction d’une matrice utilisateur–items
* Modèle basé sur **SVD (Scikit-learn)**
* Évaluation avec RMSE
* Sauvegarde du modèle entraîné :

```python
joblib.dump(model, "../models/recommender.joblib")
```

---

## **2. API FastAPI**

L’API expose un endpoint principal :

```
POST /recommend
```

Pour démarrer l’API en local :

```
uvicorn src.api.main:app --reload
```

---

## **3. Interface utilisateur Streamlit**

L'interface Streamlit permet d’interagir avec l’API déployée sur EC2 :

```
streamlit run streamlit_app/app.py
```

Fonctionnalités :

* Saisie de `user_id`
* Appel à l'API via `requests`
* Affichage clair des recommandations retournées

---

## **4. Containerisation avec Docker**

### **API FastAPI**

```
docker build -t movie-recommender .
docker run -p 8000:8000 movie-recommender
```

### **Interface Streamlit**

```
docker build -f Dockerfile.streamlit -t streamlit-ui .
docker run -p 8501:8501 streamlit-ui
```

---

## **5. Déploiement des images sur AWS ECR**

Connexion à ECR :

```
aws ecr get-login-password --region eu-west-3 \
| docker login --username AWS --password-stdin <ID>.dkr.ecr.eu-west-3.amazonaws.com
```

Push des images :

```
docker tag movie-recommender:latest <ID>.dkr.ecr.eu-west-3.amazonaws.com/movie-recommender
docker push <ID>.dkr.ecr.eu-west-3.amazonaws.com/movie-recommender
```

---

## **6. Déploiement sur AWS EC2**

Instance EC2 utilisée :

* Amazon Linux 2023
* t2.micro
* Ports ouverts :

  * 22 (SSH)
  * 8000 (API FastAPI)
  * 8501 (Streamlit)

SSH depuis le PC :

```
ssh -i movie-key.pem ec2-user@<IP_PUBLIC>
```

Sur l’instance EC2 :

```
docker pull <ID>.dkr.ecr.eu-west-3.amazonaws.com/movie-recommender
docker pull <ID>.dkr.ecr.eu-west-3.amazonaws.com/streamlit-ui
```

Lancement des containers :

```
docker run -d -p 8000:8000 movie-recommender
docker run -d -p 8501:8501 streamlit-ui
```

Accès dans le navigateur :

* API : [http://13.38.11.164:8000/docs](http://13.38.11.164:8000/docs)
* Interface Streamlit : [http://13.38.11.164:8501](http://13.38.11.164:8501)

---

## **7. Pipeline CI/CD – GitHub Actions**

Secrets configurés :

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_REGION`
* `ECR_REPO`
* `EC2_HOST`
* `EC2_USER`
* `EC2_KEY` (clé .pem encodée)

Pipeline `deploy.yml` :

* Build de l'image Docker
* Push automatique vers ECR
* Connexion SSH vers EC2
* Pull de la nouvelle image
* Redémarrage automatique des containers
  → **Déploiement 100% automatique après chaque push dans main.**

---

## **8. Exécution locale complète**

Avec Docker Compose :

```
docker compose up --build
```

Accès :

* API : [http://localhost:8000/docs](http://localhost:8000/docs)
* UI : [http://localhost:8501](http://localhost:8501)

---

## **9. Fonctionnalités du système**

* Recommandation personnalisée des films
* Algorithme basé sur les préférences utilisateurs
* API rapide et moderne avec FastAPI
* Interface simple avec Streamlit
* Déploiement cloud (AWS EC2 + ECR)
* CI/CD automatique sur GitHub Actions
* Architecture propre et modulaire

---

# **Membres du projet**

* **Hiba Hamid**
* **Ayoub Bellouch**
* **Khaoula Mafkoud**
* **Berkani Mohammed Adam**

---





