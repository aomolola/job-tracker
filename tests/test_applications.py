

def test_create_application(app_client):
    response = app_client.post(
        "/api/v1/applications",
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


def test_get_applications(app_client):
    response = app_client.get("/api/v1/applications")

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

def test_get_application(app_client):
    create_response = app_client.post(
        "/api/v1/applications",
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

    response = app_client.get(
        f"/api/v1/applications/{application_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == application_id
    assert data["company"] == "Pytest Test Company"
    assert data["position"] == "Backend Engineer"
    assert data["status"] == "Interview"
    assert data["salary"] == 100000
    assert data["experience"] == 2

def test_get_application_not_found(app_client):
    response = app_client.get("/api/v1/applications/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found"
    }


def test_update_application(app_client):
    create_response = app_client.post(
        "/api/v1/applications",
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

    update_response = app_client.put(
        f"/api/v1/applications/{application_id}",
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


def test_delete_application(app_client):
    create_response = app_client.post(
        "/api/v1/applications",
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

    delete_response = app_client.delete(
        f"/api/v1/applications/{application_id}"
    )

    assert delete_response.status_code == 200

    assert delete_response.json() == {
        "message": "Application deleted successfully"
    }

    get_response = app_client.get(
        f"/api/v1/applications/{application_id}"
    )

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Application not found"
    }


def test_delete_application_not_found(app_client):
    response = app_client.delete("/api/v1/applications/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found"
    }

def test_create_application_negative_salary(app_client):
    response = app_client.post(
        "/api/v1/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": -50000,
            "experience": 1
        }
    )

    assert response.status_code == 422



def test_create_application_invalid_status(app_client):
    response = app_client.post(
        "/api/v1/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "banana",
            "salary": 90000,
            "experience": 1
        }
    )

    assert response.status_code == 422



def test_create_application_missing_field(app_client):
    response = app_client.post(
        "/api/v1/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 90000
        }
    )

    assert response.status_code == 422


def test_filter_applications_by_status(app_client):
    response = app_client.get(
        "/api/v1/applications?status=Interview"
    )

    assert response.status_code == 200

    data = response.json()

    for application in data["applications"]:
        assert application["status"] == "Interview"

def test_filter_applications_by_company(app_client):
    response = app_client.get(
        "/api/v1/applications?company=Google"
    )

    assert response.status_code == 200

    data = response.json()

    for application in data["applications"]:
        assert application["company"] == "Google"
    
def test_search_applications(app_client):
    response = app_client.get(
        "/api/v1/applications?search=developer"
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


def test_application_pagination(app_client):
    response = app_client.get(
        "/api/v1/applications?page=1&limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 2
    assert len(data["applications"]) <= 2
    assert data["total"] >= 0
    assert data["total_pages"] >= 0


def test_application_pagination_page_two(app_client):
    response = app_client.get(
        "/api/v1/applications?page=2&limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert data["limit"] == 2
    assert len(data["applications"]) <= 2
    assert data["total"] >= 0
    assert data["total_pages"] >= 0


def test_create_application_negative_experience(app_client):
    response = app_client.post(
        "/api/v1/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 90000,
            "experience": -1
        }
    )

    assert response.status_code == 422


def test_application_pagination_invalid_parameters(app_client):
    response = app_client.get(
        "/api/v1/applications?page=0&limit=101"
    )

    assert response.status_code == 422

def test_create_application_with_deadline(app_client):
    response = app_client.post(
        "/api/v1/applications",
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

def test_create_application_with_notes(app_client):
    response = app_client.post(
        "/api/v1/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 95000,
            "experience": 1,
            "notes": "Applied through the company careers page.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Pytest Test Company"
    assert data["notes"] == "Applied through the company careers page."

def test_update_application_notes(app_client):
    create_response = app_client.post(
        "/api/v1/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 90000,
            "experience": 1,
        },
    )

    assert create_response.status_code == 200

    application_id = create_response.json()["id"]

    update_response = app_client.put(
        f"/api/v1/applications/{application_id}",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Interview",
            "salary": 90000,
            "experience": 1,
            "notes": "Interview scheduled with the engineering team.",
        },
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["application"]["notes"] == (
        "Interview scheduled with the engineering team."
    )

def test_create_application_with_interview_date(app_client):
    response = app_client.post(
        "/api/v1/applications",
        json={
            "company": "Pytest Test Company",
            "position": "Software Engineer",
            "status": "Interview",
            "salary": 95000,
            "experience": 1,
            "interview_date": "2026-10-20",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["company"] == "Pytest Test Company"
    assert data["interview_date"] == "2026-10-20"


def test_get_upcoming_deadlines(app_client):
    app_client.post(
        "/api/v1/applications",
        json={
            "company": "Past Deadline Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 90000,
            "experience": 1,
            "deadline": "2020-01-01",
        },
    )

    app_client.post(
        "/api/v1/applications",
        json={
            "company": "Later Deadline Company",
            "position": "Backend Engineer",
            "status": "Applied",
            "salary": 100000,
            "experience": 2,
            "deadline": "2099-12-31",
        },
    )

    app_client.post(
        "/api/v1/applications",
        json={
            "company": "Sooner Deadline Company",
            "position": "Python Developer",
            "status": "Applied",
            "salary": 95000,
            "experience": 1,
            "deadline": "2099-01-01",
        },
    )

    response = app_client.get("/api/v1/applications/deadlines")

    assert response.status_code == 200

    data = response.json()

    companies = [
        application["company"]
        for application in data
    ]

    assert "Past Deadline Company" not in companies
    assert "Sooner Deadline Company" in companies
    assert "Later Deadline Company" in companies

    sooner_index = companies.index(
        "Sooner Deadline Company"
    )

    later_index = companies.index(
        "Later Deadline Company"
    )

    assert sooner_index < later_index

def test_get_applications_sorted_by_deadline(app_client):
    app_client.post(
        "/api/v1/applications",
        json={
            "company": "Later Deadline Company",
            "position": "Backend Engineer",
            "status": "Applied",
            "salary": 100000,
            "experience": 2,
            "deadline": "2099-12-31",
        },
    )

    app_client.post(
        "/api/v1/applications",
        json={
            "company": "Sooner Deadline Company",
            "position": "Python Developer",
            "status": "Applied",
            "salary": 95000,
            "experience": 1,
            "deadline": "2099-01-01",
        },
    )

    response = app_client.get(
        "/api/v1/applications?sort_by=deadline&limit=100"
    )

    assert response.status_code == 200

    data = response.json()

    companies = [
        application["company"]
        for application in data["applications"]
    ]

    sooner_index = companies.index(
        "Sooner Deadline Company"
    )

    later_index = companies.index(
        "Later Deadline Company"
    )

    assert sooner_index < later_index

def test_get_applications_sorted_by_company(app_client):
    app_client.post(
        "/api/v1/applications",
        json={
            "company": "Zebra Technologies",
            "position": "Backend Engineer",
            "status": "Applied",
            "salary": 100000,
            "experience": 2,
        },
    )

    app_client.post(
        "/api/v1/applications",
        json={
            "company": "Acme Corporation",
            "position": "Python Developer",
            "status": "Applied",
            "salary": 95000,
            "experience": 1,
        },
    )

    response = app_client.get(
        "/api/v1/applications?sort_by=company&limit=100"
    )

    assert response.status_code == 200

    data = response.json()

    companies = [
        application["company"]
        for application in data["applications"]
    ]

    acme_index = companies.index(
        "Acme Corporation"
    )

    zebra_index = companies.index(
        "Zebra Technologies"
    )

    assert acme_index < zebra_index
def test_user_cannot_access_another_users_application(app_client):
    # User A creates an application.
    create_response = app_client.post(
        "/api/v1/applications",
        json={
            "company": "Private Company",
            "position": "Backend Engineer",
            "status": "Applied",
            "salary": 100000,
            "experience": 2,
        },
    )

    assert create_response.status_code == 200
    application_id = create_response.json()["id"]

    # Register User B.
    register_response = app_client.post(
        "/api/v1/auth/register",
        json={
            "email": "second-user@example.com",
            "password": "another-secure-password",
        },
    )

    assert register_response.status_code == 201

    # Log in as User B.
    login_response = app_client.post(
        "/api/v1/auth/login",
        data={
            "username": "second-user@example.com",
            "password": "another-secure-password",
        },
    )

    assert login_response.status_code == 200
    second_user_token = login_response.json()["access_token"]

    # Switch the client to User B.
    app_client.headers.update(
        {"Authorization": f"Bearer {second_user_token}"}
    )

    # User B must not be able to access User A's application.
    response = app_client.get(
        f"/api/v1/applications/{application_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"


def test_user_cannot_update_another_users_application(app_client):
    # User A creates an application.
    create_response = app_client.post(
        "/api/v1/applications",
        json={
            "company": "Private Company",
            "position": "Backend Engineer",
            "status": "Applied",
            "salary": 100000,
            "experience": 2,
        },
    )
    assert create_response.status_code == 200
    application_id = create_response.json()["id"]

    # Register and log in as User B.
    register_response = app_client.post(
        "/api/v1/auth/register",
        json={
            "email": "update-user@example.com",
            "password": "another-secure-password",
        },
    )
    assert register_response.status_code == 201

    login_response = app_client.post(
        "/api/v1/auth/login",
        data={
            "username": "update-user@example.com",
            "password": "another-secure-password",
        },
    )
    assert login_response.status_code == 200

    app_client.headers.update(
        {
            "Authorization": (
                f"Bearer {login_response.json()['access_token']}"
            )
        }
    )

    # User B attempts to update User A's application.
    response = app_client.put(
        f"/api/v1/applications/{application_id}",
        json={
            "company": "Stolen Company",
            "position": "CEO",
            "status": "Applied",
            "salary": 999999,
            "experience": 10,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"


def test_user_cannot_delete_another_users_application(app_client):
    # User A creates an application.
    create_response = app_client.post(
        "/api/v1/applications",
        json={
            "company": "Protected Company",
            "position": "Software Engineer",
            "status": "Applied",
            "salary": 85000,
            "experience": 2,
        },
    )
    assert create_response.status_code == 200
    application_id = create_response.json()["id"]

    # Register and log in as User B.
    register_response = app_client.post(
        "/api/v1/auth/register",
        json={
            "email": "delete-user@example.com",
            "password": "another-secure-password",
        },
    )
    assert register_response.status_code == 201

    login_response = app_client.post(
        "/api/v1/auth/login",
        data={
            "username": "delete-user@example.com",
            "password": "another-secure-password",
        },
    )
    assert login_response.status_code == 200

    app_client.headers.update(
        {
            "Authorization": (
                f"Bearer {login_response.json()['access_token']}"
            )
        }
    )

    # User B attempts to delete User A's application.
    response = app_client.delete(
        f"/api/v1/applications/{application_id}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"
