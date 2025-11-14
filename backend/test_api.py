"""Test API endpoints"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("Testing API...")
print()

# Test 1: Health check
print("[1] Testing health endpoint...")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ Health check passed!")
except Exception as e:
    print(f"❌ Health check failed: {e}")
print()

# Test 2: Create game
print("[2] Testing create game...")
try:
    payload = {
        "player_names": ["TestPlayer"],
        "ai_players": ["aggressive", "conservative"],
        "small_blind": 5,
        "big_blind": 10,
        "starting_stack": 1000
    }
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/api/games", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        print("✅ Create game passed!")
        game_id = data['game_id']
        
        # Test 3: Start hand
        print()
        print("[3] Testing start hand...")
        response = requests.post(f"{BASE_URL}/api/games/{game_id}/start")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Start hand passed!")
        else:
            print(f"❌ Start hand failed: {response.text}")
    else:
        print(f"❌ Create game failed: {response.text}")
        
except Exception as e:
    print(f"❌ Create game failed: {e}")
    import traceback
    traceback.print_exc()

