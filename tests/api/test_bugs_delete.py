def test_excluir_bug(api_request, auth_headers):

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
    delete_response = api_request.delete(
        f"/bugs/{bug_id}",
        headers=auth_headers
    )

    print(f"Status Code do DELETE: {delete_response.status}")

    # Assert
    assert delete_response.status == 204

    get_response = api_request.get(
        f"/bugs/{bug_id}",
        headers=auth_headers
    )

    print(f"Status Code do GET após DELETE: {get_response.status}")

    assert get_response.status == 404