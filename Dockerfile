# ---- Image de base ----
FROM python:3.11-slim

# ---- Dossier de travail ----
WORKDIR /app

# ---- Copier requirements ----
COPY requirements.txt .

# ---- Installer les dépendances ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copier le code ----
COPY src/ ./src/
COPY models/ ./models/

# ---- Mettre src dans PYTHONPATH ----
ENV PYTHONPATH="/app/src"

# ---- Exposer le port ----
EXPOSE 8000

# ---- Commande pour lancer l’API ----
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
