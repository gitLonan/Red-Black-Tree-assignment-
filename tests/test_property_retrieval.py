import requests


class TestPropertyRetrieval():

    URL = "http://127.0.0.1:5000/building"

    def test_retrieval(self):
        response = requests.get(f"{TestPropertyRetrieval.URL}/2")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_str_as_param(self):
        response = requests.get(f"{TestPropertyRetrieval.URL}/a")
        assert response.status_code == 400
