from playwright.sync_api import APIRequestContext


def test_login(api_request: APIRequestContext):

    # Arrange
    credentials = {
        "email": "qa@example.com",
        "password": "123456"
    }

    # Act
    response = api_request.post(
        "/auth/login",
        data=credentials
    )

    print(f"\nStatus Code: {response.status}")

    # Assert
    assert response.status == 200

    body = response.json()

    assert "access_token" in body
    assert body["access_token"]

    print("Token gerado com sucesso:")
    print(body["access_token"])