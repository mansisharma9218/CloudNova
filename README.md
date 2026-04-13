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
