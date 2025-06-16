import requests

def get_token():
    login_data = {"username": "test", "password": "test"}
    response = requests.post("http://localhost:5000/login", json=login_data)
    return response.json()["access_token"]

class TestPropertyUpdate:

    URL = "http://127.0.0.1:5000/property"

    def test_update_property_200(self):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                    }
        data = {
                "square_footage": 100.0,
                "rooms": 6.0
                }
        response = requests.put(f"{TestPropertyUpdate.URL}/2", headers=headers, json=data)
        assert response.status_code == 200  
        assert isinstance(response.json(), dict)

    def test_update_property_wrong_type_id(self):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                    }
        
        response = requests.put(f"{TestPropertyUpdate.URL}/a", headers=headers)
        assert response.status_code == 400

    def test_property_not_found(self):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                    }
        response = requests.put(f"{TestPropertyUpdate.URL}/999999999", headers=headers)
        assert response.status_code == 404

    def test_wrong_payload_type(self):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}",
                    "Content-Type": "text/plain"
                    }
        response = requests.put(f"{TestPropertyUpdate.URL}/2", headers=headers)
        assert response.status_code == 415
    
    def test_wrong_properties(self):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                    }
        data = {
                "square": 100.0,
                "roms": 6.0
                }
        response = requests.put(f"{TestPropertyUpdate.URL}/2", headers=headers, json=data)
        assert response.status_code == 400
        

class TestPropertyManagement:

    URL = "http://127.0.0.1:5000/property/management"

    def test_wrong_payload_type(self):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}",
                    "Content-Type": "text/plain"
                    }
        response = requests.put(TestPropertyUpdate.URL, headers=headers)
        assert response.status_code == 404

    def test_missing_fields(self):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                    }
        data = {"square_footage": 120.5,
                "construction_year": 2020,
                "land_area": 200.0,
                "registration": True,
                "rooms": 3,
                "bathrooms": 2,}
        
        response = requests.put(TestPropertyUpdate.URL, headers=headers, json=data)
        assert response.status_code == 404

    def test_wrong_fields(self):
        token = get_token()
        headers = {"Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                    }
        data = {"square_footage": 120.5,
                "construction_year": 2020,
                "land_area": 200.0,
                "registration": True,
                "rooms": 3,
                "bathrooms": 2,
                "parkin": True,
                "price": 250000,
                "estate_type_id": 1,
                "offer_id": 2,
                "city_part_id": 5}
        
        response = requests.put(TestPropertyUpdate.URL, headers=headers, json=data)
        assert response.status_code == 404
    
        
    