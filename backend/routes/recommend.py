from fastapi import APIRouter, Depends
from auth import verify_token
from routes.predict import predict_cost

router = APIRouter()

@router.post("/")
def get_recommendation(
    vcpu:          int,
    ram_gb:        float,
    storage_gb:    float,
    usage_hours:   float,
    region:        str   = "us-east",
    pricing_model: str   = "on-demand",
    budget:        float = None,
    user = Depends(verify_token)
):
    costs = {
        "AWS":   predict_cost(vcpu, ram_gb, storage_gb, usage_hours, "AWS",   region, pricing_model),
        "Azure": predict_cost(vcpu, ram_gb, storage_gb, usage_hours, "Azure", region, pricing_model),
        "GCP":   predict_cost(vcpu, ram_gb, storage_gb, usage_hours, "GCP",   region, pricing_model),
    }

    sorted_providers = sorted(costs.items(), key=lambda x: x[1])
    best             = sorted_providers[0]
    worst            = sorted_providers[-1]
    savings          = round(worst[1] - best[1], 2)

    recommendations = []

    recommendations.append({
        "type":     "cost",
        "priority": "high",
        "message":  f"{best[0]} is the cheapest at ${best[1]}/month for your workload.",
    })

    recommendations.append({
        "type":     "savings",
        "priority": "high",
        "message":  f"Switch from {worst[0]} to {best[0]} and save ${savings}/month.",
    })

    if budget and best[1] > budget:
        recommendations.append({
            "type":     "budget",
            "priority": "critical",
            "message":  f"Cheapest option ${best[1]}/month exceeds your budget of ${budget}. Consider reducing storage or usage hours.",
        })

    if usage_hours < 360:
        recommendations.append({
            "type":     "usage",
            "priority": "medium",
            "message":  "You are using less than 50% of monthly hours. Consider spot instances for extra savings.",
        })

    if pricing_model == "on-demand" and usage_hours >= 500:
        recommendations.append({
            "type":     "pricing",
            "priority": "medium",
            "message":  f"You are running {usage_hours} hours/month. Switching to 1yr-reserved could save you ~55% compared to on-demand.",
        })

    return {
        "best_provider":   best[0],
        "costs":           costs,
        "recommendations": recommendations,
    }