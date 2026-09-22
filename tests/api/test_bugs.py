def test_acessar_bugs(api_request, auth_headers):

    # Act
    response = api_request.get(
        "/bugs",
        headers=auth_headers
    )

    print(f"\nStatus Code: {response.status}")

    # Assert
    assert response.status == 200