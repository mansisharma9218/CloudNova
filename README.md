# CloudNova — Smart Cloud Resource Advisor

## Overview

CloudNova is a full-stack web application that helps developers, startups, and businesses find the most cost-effective cloud provider for their workload. By taking in key resource requirements as inputs, the platform uses a trained Machine Learning model to predict monthly costs across AWS, Azure, and GCP and recommends the optimal provider based on real pricing patterns.

Traditional cloud cost estimation is manual, time-consuming, and often inaccurate. CloudNova eliminates this by providing an intelligent, data-driven recommendation engine backed by real and verified pricing data.

## Objectives

- Predict monthly cloud costs across AWS, Azure, and GCP using a trained ML model.
- Recommend the most cost-effective provider based on user workload requirements.
- Visualize cost comparisons across providers in an intuitive dashboard.
- Provide authenticated access with Google Sign-In via Firebase.
- Expose a secure, token-protected REST API backend.

## Key Features

### 1. Google Authentication
Secure login via Firebase Google Sign-In. All API endpoints are protected with Firebase ID token verification — only authenticated users can access predictions and pricing data.

### 2. ML-Powered Cost Prediction
A Random Forest Regressor trained on 24,000+ records predicts monthly costs for each provider given the user's resource configuration. The model achieves an R² of 0.9874 and MAE of ~$13, making it highly accurate for general-purpose workloads.

### 3. Provider Comparison Dashboard
Users configure their workload using 6 inputs and click Predict & Compare to instantly see side-by-side cost predictions for AWS, Azure, and GCP with visual bar charts and a clear best-provider recommendation.

### 4. Pricing Table
A filterable table of real cloud instance types across all three providers, fetched from the database, allowing users to browse and compare specific instance configurations.

### 5. Trends Page
Line charts showing 6-month cost trends and a radar chart comparing provider capabilities across multiple dimensions.

### 6. Secure Backend API
A FastAPI backend with Firebase token verification on all routes. Endpoints for prediction, recommendations, and pricing data are all protected and CORS-configured for the frontend.

## Inputs

The ML model and prediction API accept the following 6 inputs:

| Input | Description |
|-------|-------------|
| vCPU | Number of virtual CPU cores |
| RAM (GB) | Memory in gigabytes |
| Storage (GB) | Disk storage in gigabytes |
| Usage Hours/Month | Hours the instance will run per month (1–744) |
| Pricing Model | on-demand / 1yr-reserved / 3yr-reserved / spot |
| Region | us-east / us-west / europe / asia |

## Tech Stack

**Frontend**
- React.js
- Recharts (data visualization)
- Firebase Authentication
- Custom CSS (no UI framework)

**Backend**
- FastAPI (Python)
- SQLAlchemy ORM
- Firebase Admin SDK (token verification)
- Uvicorn

**Database**
- PostgreSQL

**Machine Learning**
- scikit-learn (Random Forest Regressor)
- pandas, numpy
- pickle (model serialization)

**Data Sources**
- AWS Bulk Pricing API (on-demand, us-east-1) 
- Azure Retail Prices API (on-demand, per region) 
- GCP public pricing data
- Reserved and spot pricing calculated using verified discount multipliers from official AWS and Azure documentation
- Regional multipliers derived from official AWS regional pricing documentation

## ML Model

| Metric | Value |
|--------|-------|
| Algorithm | Random Forest Regressor |
| Training Records | 24,855 |
| R² Score | 0.9958 |
| MAE | $0.0162/hr |
| Features | vcpu, ram_gb, storage_gb, provider, region, pricing_model |

### Feature Importance
```
vcpu               75.8%
ram_gb             14.8%
pricing_model       9.0%
provider            0.1%
region              0.5%
storage_gb          0.2%
```

### Model Notes
- Training data covers general-purpose instance families across all three providers
- Dataset balanced to equal representation per provider per pricing model
- Categorical features (provider, region, pricing_model) encoded using LabelEncoder
- Model and encoders serialized using pickle for backend inference

## Project Structure
```
cloud-advisor/
├── frontend/
│   ├── public/
│   └── src/
│       ├── api/
│       │   └── cloudApi.js
│       ├── components/
│       │   ├── Navbar.jsx
│       │   ├── Slider.jsx
│       │   ├── StatCard.jsx
│       │   └── ProviderBars.jsx
│       ├── constants/
│       │   ├── providerColors.js
│       │   └── ChartTooltipStyle.js
│       ├── pages/
│       │   ├── AdvisorPage.jsx
│       │   ├── PricingPage.jsx
│       │   ├── TrendsPage.jsx
│       │   └── LoginPage.jsx
│       ├── firebase.js
│       ├── index.js
│       └── styles/global.css
├── backend/
│   ├── routes/
│   │   ├── predict.py
│   │   ├── pricing.py
│   │   ├── trends.py
│   │   └── recommend.py
│   ├── utils/
│   │   └── cost_utils.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── seed.py
│   └── main.py
└── ml_model/
    ├── fetch_prices.py
    ├── train.py
    ├── data.csv
    ├── cost_model.pkl
    └── encoders.pkl
```

## Installation Guide

### Prerequisites

- Node.js v18+
- Python 3.12+
- PostgreSQL 15+
- A Firebase project with Google Sign-In enabled

### 1. Clone the Repository
```bash
git clone https://github.com/mansisharma9218/CloudNova.git
cd CloudNova
```

### 2. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary pandas scikit-learn python-dotenv firebase-admin
```

Create `backend/.env`:
```
DATABASE_URL=postgresql://your_username@localhost/cloudnova
```

Place your Firebase service account key at `backend/firebase_key.json`.

Create the database:
```bash
psql -U your_username -c "CREATE DATABASE cloudnova;"
```

Start the backend:
```bash
uvicorn main:app --reload
```

### 3. ML Model Setup
```bash
cd ..
source backend/venv/bin/activate
python ml_model/fetch_prices.py
python ml_model/train.py
```

### 4. Frontend Setup
```bash
cd frontend
npm install
```

Create `frontend/.env`:
```
REACT_APP_FIREBASE_API_KEY=your_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your_auth_domain
REACT_APP_FIREBASE_PROJECT_ID=your_project_id
REACT_APP_FIREBASE_STORAGE_BUCKET=your_storage_bucket
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
REACT_APP_FIREBASE_APP_ID=your_app_id
```

Start the frontend:
```bash
npm start
```

### 5. Access the App
```
Frontend:  http://localhost:3000
Backend:   http://localhost:8000
API Docs:  http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | Health check | No |
| POST | `/api/predict/` | Predict costs for all 3 providers | Yes |
| POST | `/api/recommend/` | Get recommendations with savings tips | Yes |
| GET | `/api/pricing/` | Get all pricing data from database | Yes |
| GET | `/api/pricing/{provider}` | Get pricing filtered by provider | Yes |
| GET | `/api/trends/` | Get 6 month predicted cost trend | Yes |

All protected endpoints require a Firebase ID token in the Authorization header:
```
Authorization: Bearer <firebase_id_token>
```

## Future Enhancements

- Docker containerization with docker-compose
- Cloud deployment (AWS/GCP/Azure)
- User prediction history stored per account
- Real-time GCP pricing via Google Cloud Billing API
- Retrain model periodically with updated pricing data
