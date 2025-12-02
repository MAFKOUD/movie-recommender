from fastapi import FastAPI
from pydantic import BaseModel
from recommender.model import recommend_movies

app = FastAPI()

class RecommendRequest(BaseModel):
    user_id: int
    top_k: int = 10

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/recommend")
def recommend(req: RecommendRequest):
    recs = recommend_movies(req.user_id, req.top_k)
    return {"user_id": req.user_id, "recommendations": recs}
