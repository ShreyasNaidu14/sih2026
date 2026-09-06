import requests

# Replace with the actual URL obtained from Render or Railway
BASE_URL = "https://mahakrishi-api.onrender.com"

def test_deployment():
    print(f"Pinging {BASE_URL}...")
    
    try:
        health_check = requests.get(f"{BASE_URL}/health")
        print(f"/health status: {health_check.status_code}")
        
        listings_check = requests.get(f"{BASE_URL}/api/marketplace/listings")
        print(f"/api/marketplace/listings status: {listings_check.status_code}")
        
        if listings_check.status_code == 200:
            print("Deployment verified: Endpoints are active and reachable.")
    except Exception as e:
        print(f"Error connecting to deployment: {e}")

if __name__ == "__main__":
    test_deployment()