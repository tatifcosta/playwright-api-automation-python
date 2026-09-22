def test_consultar_bug_por_id(api_request, auth_headers):

    # Arrange
    payload = {
        "title": "Coluna Data de Atualização apresenta valor divergente do registro",
        "description": "A coluna 'Data de Atualização' da página de listagem apresenta uma data diferente da registrada no detalhe do item. O valor exibido na listagem não corresponde à última atualização realizada.",
        "priority": "HIGH",
        "status": "OPEN"
    }

    post_response = api_request.post(
        "/bugs",
        headers=auth_headers,
        data=payload
    )

    assert post_response.status == 201

    created_bug = post_response.json()
    bug_id = created_bug["id"]

    print(f"\nBug criado com ID: {bug_id}")

    # Act
    get_response = api_request.get(
        f"/bugs/{bug_id}",
        headers=auth_headers
    )

    print(f"Status Code: {get_response.status}")

    # Assert
    assert get_response.status == 200

    body = get_response.json()

    print("Response da API:")
    print(body)

    assert body["id"] == bug_id
    assert body["title"] == payload["title"]
    assert body["description"] == payload["description"]
    assert body["priority"] == payload["priority"]
    assert body["status"] == payload["status"]


def test_deve_retornar_404_ao_consultar_bug_inexistente(
    api_request,
    auth_headers
):

    # Arrange
    bug_id_inexistente = 999999

    # Act
    response = api_request.get(
        f"/bugs/{bug_id_inexistente}",
        headers=auth_headers
    )

    print(f"\nStatus Code: {response.status}")

    # Assert
    assert response.status == 404