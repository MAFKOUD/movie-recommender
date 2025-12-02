import streamlit as st
import requests
import pandas as pd

# URL de ton API déployée sur EC2
API_URL = "http://13.38.11.164:8000/recommend"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬")
st.title("🎬 Movie Recommender")
st.write("Entrez un `user_id` et obtenez les films recommandés par votre modèle déployé sur AWS.")

# --- Entrées utilisateur ---
user_id = st.number_input("User ID", min_value=1, value=1, step=1)
top_k = st.slider("Nombre de films recommandés (top_k)", min_value=1, max_value=20, value=10, step=1)

if st.button("Obtenir des recommandations"):
    payload = {
        "user_id": int(user_id),
        "top_k": int(top_k)
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)

        if response.status_code == 200:
            data = response.json()

            recs = data.get("recommendations", [])

            if not recs:
                st.warning("Aucune recommandation retournée par l'API.")
            else:
                # On transforme la liste en DataFrame pour un affichage propre
                df = pd.DataFrame(recs)
                # On arrondit les scores
                if "pred_rating" in df.columns:
                    df["pred_rating"] = df["pred_rating"].round(3)

                st.success(f"Recommandations pour l'utilisateur {data.get('user_id')}:")
                st.dataframe(df[["title", "pred_rating"]].rename(columns={
                    "title": "Titre du film",
                    "pred_rating": "Score prédit"
                }))
        else:
            st.error(f"Erreur HTTP {response.status_code}")
            st.code(response.text)

    except Exception as e:
        st.error("Erreur lors de l'appel à l'API.")
        st.exception(e)
