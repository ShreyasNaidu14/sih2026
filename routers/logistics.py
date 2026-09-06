from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/logistics", tags=["MahaVahan Logistics"])

# 1. Corridor Route Generator Data
pooled_route = {
    "route_id": "MH-ROUTE-102",
    "corridor_name": "Nashik Onion & Fresh Produce Export Corridor",
    "vehicle_number": "MH-15-EG-4412",
    "driver_name": "Suresh Shinde",
    "driver_phone": "+91-9822012345",
    "total_capacity_tonnes": 16.0,
    "booked_tonnes": 12.5,
    "available_tonnes": 3.5,
    "utilization_rate": "78.1%",
    "waypoints": [
        {"name": "Lasalgaon Onion FPO", "lat": 20.1466, "lng": 74.2255, "action": "Pickup", "tonnes": 6.5},
        {"name": "Pimpalgaon Baswant Hub", "lat": 20.1706, "lng": 73.9847, "action": "Pickup", "tonnes": 4.0},
        {"name": "Nashik Central APMC", "lat": 19.9975, "lng": 73.7898, "action": "Pickup", "tonnes": 2.0},
        {"name": "Igatpuri Highway Checkpoint", "lat": 19.6983, "lng": 73.5606, "action": "Transit"},
        {"name": "JNPT Export Terminal, Navi Mumbai", "lat": 18.9499, "lng": 72.9515, "action": "Unload", "tonnes": 12.5}
    ]
}

# Request model for farmer pickup
class PoolRequest(BaseModel):
    farmer_name: str
    location_lat: float
    location_lng: float
    weight_tonnes: float

@router.get("/routes")
def get_pooled_routes():
    """Returns active pooled routes with full waypoints and utilization stats."""
    return [pooled_route]

@router.post("/pool-request")
def request_pool(request: PoolRequest):
    """Accepts farmer pickup request and checks capacity."""
    if request.weight_tonnes > pooled_route["available_tonnes"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Only {pooled_route['available_tonnes']} tonnes available. Request exceeds capacity."
        )
    
    return {
        "status": "Success",
        "message": f"Booking confirmed for {request.farmer_name}.",
        "booked_tonnes": request.weight_tonnes,
        "cost_savings": "Saved ₹3,800 vs private booking"
    }