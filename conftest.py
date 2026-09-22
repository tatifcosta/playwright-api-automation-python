import pytest
from playwright.sync_api import Playwright


BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture
def api_request(playwright: Playwright):
    request = playwright.request.new_context(
        base_url=BASE_URL
    )

    yield request

    request.dispose()


@pytest.fixture
def token(api_request):
    response = api_request.post(
        "/auth/login",
        data={
            "email": "qa@example.com",
            "password": "123456"
        }
    )

    assert response.status == 200

    body = response.json()

    return body["access_token"]

@pytest.fixture
def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }