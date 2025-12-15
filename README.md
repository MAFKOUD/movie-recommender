# 🎬 Movie Recommender System – MLOps Project

Ce projet implémente un système complet de recommandation de films basé sur le dataset **MovieLens**.  
Il comprend :

- un modèle de Machine Learning,
- une API **FastAPI**,
- une interface utilisateur **Streamlit**,
- une containerisation **Docker**,
- un déploiement cloud sur **AWS (ECR + ECS Fargate)**,
- et un pipeline **CI/CD avec GitHub Actions**.

---

## 1. Entraînement du modèle (Notebook)

Le notebook d’entraînement se trouve dans :

```

notebooks/training.ipynb

````

Étapes réalisées :

- Chargement du dataset **MovieLens 100K**
- Nettoyage et préprocessing des données
- Construction d’une matrice utilisateur–items
- Modèle de recommandation basé sur **SVD (Scikit-learn)**
- Évaluation du modèle avec la métrique **RMSE**
- Sauvegarde du modèle entraîné :

```python
joblib.dump(model, "../models/recommender.joblib")
````

Le modèle sauvegardé est ensuite utilisé par l’API FastAPI.

---

## 2. API FastAPI

L’API expose un endpoint principal :

```
POST /recommend
```

Démarrage de l’API en local :

```bash
uvicorn src.api.main:app --reload
```

L’API charge le modèle entraîné et retourne des recommandations personnalisées à partir d’un `user_id`.

---

## 3. Interface utilisateur Streamlit

L’interface **Streamlit** permet d’interagir avec l’API déployée sur **AWS ECS**.

Démarrage en local :

```bash
streamlit run app.py
```

Fonctionnalités :

* Saisie du `user_id`
* Appel de l’API FastAPI via `requests`
* Affichage clair et lisible des recommandations retournées

---

## 4. Containerisation avec Docker

### API FastAPI

```bash
docker build -t movie-recommender .
docker run -p 8000:8000 movie-recommender
```

### Interface Streamlit

```bash
docker build -f Dockerfile.streamlit -t streamlit-ui .
docker run -p 8501:8501 streamlit-ui
```

Chaque composant (API et UI) est isolé dans son propre conteneur Docker.

---

## 5. Déploiement des images sur AWS ECR

Connexion au registre **Amazon ECR** :

```bash
aws ecr get-login-password --region eu-west-3 \
| docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com
```

Push des images Docker :

```bash
docker tag movie-recommender:latest <ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com/movie-recommender
docker push <ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com/movie-recommender

docker tag streamlit-ui:latest <ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com/streamlit-ui
docker push <ACCOUNT_ID>.dkr.ecr.eu-west-3.amazonaws.com/streamlit-ui
```

---

## 6. Déploiement sur AWS ECS (Fargate)

Le projet est déployé sur **AWS ECS avec Fargate** (mode serverless, sans gestion de serveurs).

### Infrastructure ECS

* **Cluster ECS** : `group2-MLOpsCluster`
* **Task Definition** :

  * `movie-api` → API FastAPI (port 8000)
  * `streamlit-ui` → Interface Streamlit (port 8501)
* **Réseau** :

  * IP publique activée
  * Groupe de sécurité autorisant les ports `8000` et `8501`

### Accès à l’application

* **API FastAPI**
  👉 [http://15.237.181.203:8000/docs](http://15.237.181.203:8000/docs)

* **Interface Streamlit**
  👉 [http://15.237.181.203:8501](http://15.237.181.203:8501)
  
## Services AWS utilisés

- **Amazon ECR** : stockage des images Docker
- **Amazon ECS (Fargate)** : orchestration et exécution des conteneurs
- **Amazon CloudWatch** : logs des conteneurs ECS
- **IAM** : gestion des rôles et permissions pour ECS et CI/CD
  
## Infrastructure as Code – Terraform

L’infrastructure AWS est définie et gérée via **Terraform** :

- Backend S3 pour le stockage distant et versionné du fichier Terraform state
- Configuration du provider AWS
- Gestion reproductible de l’infrastructure

Cette approche garantit la traçabilité, la reproductibilité et l’automatisation de l’infrastructure.

---

## 7. Pipeline CI/CD – GitHub Actions (ECS)

Un pipeline **CI/CD automatique** est mis en place avec **GitHub Actions**.

### Secrets GitHub configurés

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_REGION`
* `ECR_REPOSITORY`
* `ECS_CLUSTER`
* `ECS_SERVICE`

### Fonctionnement du pipeline (`ecs-deploy.yml`)

* Build des images Docker
* Push automatique vers **Amazon ECR**
* Mise à jour du service **ECS**
* Redéploiement automatique des tâches Fargate

Chaque push sur la branche `main` déclenche automatiquement un nouveau déploiement sur ECS.

---

Accès local :

* API : [http://localhost:8000/docs](http://localhost:8000/docs)
* UI : [http://localhost:8501](http://localhost:8501)

---

## 8. Fonctionnalités du système

* Recommandation personnalisée de films
* Algorithme basé sur les préférences utilisateurs
* API moderne et performante avec FastAPI
* Interface utilisateur intuitive avec Streamlit
* Déploiement cloud serverless avec **AWS ECS Fargate**
* CI/CD entièrement automatisé
* Architecture modulaire et maintenable

---

## Membres du projet

* **Hiba Hamid**
* **Ayoub Bellouch**
* **Khaoula Mafkoud**
* **Berkani Mohammed Adam**
* **Brunel Nangoum-Tchatchoua**

```

