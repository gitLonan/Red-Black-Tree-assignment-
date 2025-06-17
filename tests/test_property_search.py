import requests
import json

class TestPropertySearch:
    

    URL = "http://127.0.0.1:5000/property/search"

    def test_search_by_property_type(self):
        response = requests.get(TestPropertySearch.URL, params={"property_type": "kuća"})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_search_by_min_sq_footage(self):
        response = requests.get(TestPropertySearch.URL, params={"min_sq_footage": 50})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_search_by_max_sq_footage(self):
        response = requests.get(TestPropertySearch.URL, params={"max_sq_footage": 100})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_search_by_parking(self):
        response = requests.get(TestPropertySearch.URL, params={"parking": "true"})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_search_by_state(self):
        response = requests.get(TestPropertySearch.URL, params={"state": "Beograd"})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_search_by_estate_type(self):
        response = requests.get(TestPropertySearch.URL, params={"estate_type": "stan"})
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_combined_search(self):
        query = {
                    "property_type": "kuća",
                    "min_sq_footage": 80,
                    "max_sq_footage": 200,
                    "parking": "true",
                    "state": "Beograd",
                    "estate_type": "kuća"
                }
        response = requests.get(TestPropertySearch.URL, params=query)
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_pagination(self):
        response = requests.get(TestPropertySearch.URL, params={"min_sq_footage": 70})
        json_data = response.json()
        assert "next_url" in json_data
        next_url = json_data["next_url"]
        response = requests.get(f"http://127.0.0.1:5000/{next_url}", params={"min_sq_footage": 70})
        assert response.status_code == 200
        
    def test_page_wrong_type(self):
        response = requests.get(TestPropertySearch.URL, params={"min_sq_footage": 70, "page": "abc"})
        #flask silently fails and translates error into page=1, because we provided with the default value
        assert response.status_code == 200