from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routes import pricing, predict, recommend
from routes import trends

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CloudNova API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trends.router, prefix="/api/trends")
app.include_router(pricing.router,   prefix="/api/pricing")
app.include_router(predict.router,   prefix="/api/predict")
app.include_router(recommend.router, prefix="/api/recommend")

@app.get("/")
def root():
    return {"message": "CloudNova API is running"}