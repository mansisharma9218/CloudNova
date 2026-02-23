from fastapi import APIRouter, Depends
from auth import verify_token

router = APIRouter()

@router.post("/")
def get_recommendation(
    vcpu: int,
    ram_gb: float,
    storage_gb: float,
    usage_hours: float,
    budget: float = None,
    user=Depends(verify_token)  # 🔐 PROTECTED
):
    base = vcpu * 8 + ram_gb * 3.5 + storage_gb * 0.08 + (usage_hours / 720) * 12

    costs = {
        "AWS":   round(base * 1.05, 2),
        "Azure": round(base * 1.02, 2),
        "GCP":   round(base * 0.96, 2),
    }

    sorted_providers = sorted(costs.items(), key=lambda x: x[1])
    best  = sorted_providers[0]
    worst = sorted_providers[-1]

    recommendations = []

    recommendations.append({
        "type":     "cost",
        "priority": "high",
        "message":  f"{best[0]} is the cheapest at ${best[1]}/month for your workload.",
    })

    savings = round(worst[1] - best[1], 2)
    recommendations.append({
        "type":     "savings",
        "priority": "high",
        "message":  f"Switch from {worst[0]} to {best[0]} and save ${savings}/month.",
    })

    if budget and best[1] > budget:
        recommendations.append({
            "type":     "budget",
            "priority": "critical",
            "message":  f"Your cheapest option ${best[1]}/month exceeds your budget of ${budget}. Consider reducing storage or usage hours.",
        })

    if usage_hours < 360:
        recommendations.append({
            "type":     "usage",
            "priority": "medium",
            "message":  "You're using less than 50% of monthly hours. Consider spot/preemptible instances for extra savings.",
        })

    return {
        "best_provider":   best[0],
        "costs":           costs,
        "recommendations": recommendations,
    }