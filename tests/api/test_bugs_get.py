def test_listar_bugs(api_request, auth_headers):

    # Arrange
    endpoint = "/bugs"

    # Act
    response = api_request.get(
        endpoint,
        headers=auth_headers
    )

    print(f"\nStatus Code: {response.status}")

    # Assert
    assert response.status == 200

    body = response.json()

    print("Response da API:")
    print(body)

    assert isinstance(body, list)