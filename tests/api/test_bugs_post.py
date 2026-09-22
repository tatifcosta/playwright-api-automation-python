def test_criar_bug(api_request, auth_headers):

    # Arrange
    payload = {
        "title": "Coluna Data de Atualização apresenta divergência no registro",
        "description": "A coluna Data de Atualização da página de listagem apresenta uma data diferente da registrada no detalhe do item. O valor exibido na listagem não corresponde à última atualização realizada.",
        "priority": "HIGH",
        "status": "OPEN"
    }

    # Act
    response = api_request.post(
        "/bugs",
        headers=auth_headers,
        data=payload
    )

    print(f"\nStatus Code: {response.status}")

    # Assert
    assert response.status == 201

    body = response.json()

    print("Response da API:")
    print(body)

    assert body["id"] is not None
    assert body["title"] == payload["title"]
    assert body["description"] == payload["description"]
    assert body["priority"] == payload["priority"]
    assert body["status"] == payload["status"]