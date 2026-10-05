from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_create_application():
    response = client.post(
        "/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 90000,
            "experience": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Pytest Test Company"
    assert data["position"] == "Software Engineer"
    assert data["status"] == "Applied"
    assert data["salary"] == 90000
    assert data["experience"] == 1


def test_get_applications():
    response = client.get("/applications")

    assert response.status_code == 200

    data = response.json()

    assert "page" in data
    assert "limit" in data
    assert "total" in data
    assert "total_pages" in data
    assert "applications" in data

    assert data["page"] == 1
    assert data["limit"] == 10
    assert isinstance(data["applications"], list)

def test_get_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Backend Engineer",
            "status": "Interview",
            "salary": 100000,
            "experience": 2
        }
    )

    assert create_response.status_code == 200

    application_id = create_response.json()["id"]

    response = client.get(
        f"/applications/{application_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == application_id
    assert data["company"] == "Pytest Test Company"
    assert data["position"] == "Backend Engineer"
    assert data["status"] == "Interview"
    assert data["salary"] == 100000
    assert data["experience"] == 2

def test_get_application_not_found():
    response = client.get("/applications/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found"
    }


def test_update_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 90000,
            "experience": 1
        }
    )

    assert create_response.status_code == 200

    application_id = create_response.json()["id"]

    update_response = client.put(
        f"/applications/{application_id}",
        json={
            "company": "Pytest Test Company",
            "position": "Senior Software Engineer",
            "status": "Interview",
            "salary": 120000,
            "experience": 3
        }
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["message"] == "Application successfully updated"
    assert data["application"]["id"] == application_id
    assert data["application"]["position"] == "Senior Software Engineer"
    assert data["application"]["status"] == "Interview"
    assert data["application"]["salary"] == 120000
    assert data["application"]["experience"] == 3


def test_delete_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 90000,
            "experience": 1
        }
    )

    assert create_response.status_code == 200

    application_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/applications/{application_id}"
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {
        "message": "Application deleted successfully"
    }

    get_response = client.get(
        f"/applications/{application_id}"
    )

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Application not found"
    }


def test_delete_application_not_found():
    response = client.delete("/applications/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found"
    }

def test_create_application_negative_salary():
    response = client.post(
        "/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": -50000,
            "experience": 1
        }
    )

    assert response.status_code == 422



def test_create_application_invalid_status():
    response = client.post(
        "/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "banana",
            "salary": 90000,
            "experience": 1
        }
    )

    assert response.status_code == 422



def test_create_application_missing_field():
    response = client.post(
        "/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 90000
        }
    )

    assert response.status_code == 422


def test_filter_applications_by_status():
    response = client.get(
        "/applications?status=Interview"
    )

    assert response.status_code == 200

    data = response.json()

    for application in data["applications"]:
        assert application["status"] == "Interview"

def test_filter_applications_by_company():
    response = client.get(
        "/applications?company=Google"
    )

    assert response.status_code == 200

    data = response.json()

    for application in data["applications"]:
        assert application["company"] == "Google"
    
def test_search_applications():
    response = client.get(
        "/applications?search=developer"
    )

    assert response.status_code == 200

    data = response.json()

    for application in data["applications"]:
        company = application["company"].lower()
        position = application["position"].lower()

        assert (
            "developer" in company
            or "developer" in position
        )


def test_application_pagination():
    response = client.get(
        "/applications?page=1&limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 2
    assert len(data["applications"]) <= 2
    assert data["total"] >= 0
    assert data["total_pages"] >= 0


def test_application_pagination_page_two():
    response = client.get(
        "/applications?page=2&limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["limit"] == 2
    assert len(data["applications"]) <= 2
    assert data["total"] >= 0
    assert data["total_pages"] >= 0


def test_create_application_negative_experience():
    response = client.post(
        "/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 90000,
            "experience": -1
        }
    )

    assert response.status_code == 422


def test_application_pagination_invalid_parameters():
    response = client.get(
        "/applications?page=0&limit=101"
    )

    assert response.status_code == 422

def test_create_application_with_deadline():
    response = client.post(
        "/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 95000,
            "experience": 1,
            "deadline": "2026-10-15",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Pytest Test Company"
    assert data["deadline"] == "2026-10-15"
