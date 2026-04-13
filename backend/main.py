from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routes import pricing, predict, recommend, insights

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CloudNova API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pricing.router,  prefix="/api/pricing")
app.include_router(predict.router,  prefix="/api/predict")
app.include_router(recommend.router,prefix="/api/recommend")
app.include_router(insights.router, prefix="/api/insights")

@app.get("/")
def root():
    return {"message": "CloudNova API is running"}
