# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# -----------------------
# Helper: get staff token
# -----------------------
def get_staff_token():
    r = client.post("/auth/token", data={"username": "alice", "password": "wonderland"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# -----------------------
# Test: Create & Get Room
# -----------------------
def test_create_and_get_room():
    headers = get_staff_token()
    
    # Create room
    payload = {"number": "102", "type": "double", "price": 120, "capacity": 2}
    r = client.post("/rooms/rooms/", json=payload, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["number"] == "102"
    rid = data["id"]

    # Get room by ID
    r2 = client.get(f"/rooms/rooms/{rid}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["number"] == "102"


# -----------------------
# Test: Update Room
# -----------------------
def test_update_room():
    headers = get_staff_token()

    # First create a room
    payload = {"number": "103", "type": "single", "price": 80, "capacity": 1}
    r = client.post("/rooms/rooms/", json=payload, headers=headers)
    rid = r.json()["id"]

    # Update room
    update_payload = {"number": "103", "type": "single", "price": 100, "capacity": 1}
    r2 = client.put(f"/rooms/rooms/{rid}", json=update_payload, headers=headers)
    assert r2.status_code == 200
    assert r2.json()["price"] == 100


# -----------------------
# Test: List Rooms
# -----------------------
def test_list_rooms():
    r = client.get("/rooms/rooms/")
    assert r.status_code == 200
    data = r.json()
    # If using pagination, check items
    assert "items" in data
    assert isinstance(data["items"], list)


# -----------------------
# Test: Delete Room
# -----------------------
def test_delete_room():
    headers = get_staff_token()

    # Create room to delete
    payload = {"number": "104", "type": "suite", "price": 200, "capacity": 3}
    r = client.post("/rooms/rooms/", json=payload, headers=headers)
    rid = r.json()["id"]

    # Delete room
    r2 = client.delete(f"/rooms/rooms/{rid}", headers=headers)
    assert r2.status_code == 200
    assert r2.json() == {"ok": True}
