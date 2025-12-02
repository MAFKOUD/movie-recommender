import joblib
from pathlib import Path
import numpy as np
import pandas as pd

# stockage des objets en mémoire (singleton)
_model = {}

def load_artifact(name):
    """
    Charge un fichier .pkl depuis le dossier models.
    """
    path = Path(__file__).resolve().parent.parent.parent / "models" / name
    return joblib.load(path)


def get_model():
    """
    Charge les matrices P, Q et les mappings une seule fois.
    """
    global _model

    if not _model:
        print("Loading model artifacts...")

        _model["P"] = load_artifact("P_trained.pkl")
        _model["Q"] = load_artifact("Q_trained.pkl")
        _model["user2idx"] = load_artifact("user2idx.pkl")
        _model["item2idx"] = load_artifact("item2idx.pkl")
        _model["movies_df"] = load_artifact("movies_df.pkl")
        _model["train_df"] = load_artifact("train_df.pkl")

        print("Model loaded.")

    return _model


def recommend_movies(user_id, top_n=10):
    """
    Fait la recommandation top-N en appelant la logique de ton notebook.
    """
    m = get_model()

    P = m["P"]
    Q = m["Q"]
    user2idx = m["user2idx"]
    item2idx = m["item2idx"]
    movies_df = m["movies_df"]
    R_df = m["train_df"]

    if user_id not in user2idx:
        return {"error": "User not found"}

    u_idx = user2idx[user_id]
    user_vector = P[u_idx]

    # vecteurs item
    all_items = movies_df["item_id"].values
    item_vectors = []

    for iid in all_items:
        if iid in item2idx:
            item_vectors.append(Q[item2idx[iid]])
        else:
            # item non présent dans l'entraînement
            item_vectors.append(np.random.randn(Q.shape[1]) * 0.01)

    item_vectors = np.array(item_vectors)

    # prédictions
    pred_ratings = item_vectors.dot(user_vector)

    items_pred = pd.DataFrame({
        "item_id": all_items,
        "pred_rating": pred_ratings
    })

    # retirer les films déjà vus
    seen = R_df[R_df["user_id"] == user_id]["item_id"].tolist()
    items_pred = items_pred[~items_pred["item_id"].isin(seen)]

    # joindre les titres
    items_pred = items_pred.merge(movies_df, on="item_id")

    # top N
    top_movies = items_pred.sort_values("pred_rating", ascending=False).head(top_n)

    # convertir en JSON
    return top_movies[["item_id", "title", "pred_rating"]].to_dict(orient="records")
