def test_atualizar_bug(api_request, auth_headers):

    # Arrange
    payload_criacao = {
        "title": "Coluna Data de Atualização apresenta valor divergente do registro",
        "description": "A coluna 'Data de Atualização' da página de listagem apresenta uma data diferente da registrada no detalhe do item. O valor exibido na listagem não corresponde à última atualização realizada.",
        "priority": "HIGH",
        "status": "OPEN"
    }

    post_response = api_request.post(
        "/bugs",
        headers=auth_headers,
        data=payload_criacao
    )

    assert post_response.status == 201

    created_bug = post_response.json()
    bug_id = created_bug["id"]

    print(f"\nBug criado com ID: {bug_id}")

    payload_atualizacao = {
        "title": "Coluna Data de Atualização apresenta valor divergente do registro",
        "description": "Após nova análise, foi confirmado que a divergência ocorre quando o registro é atualizado.",
        "priority": "CRITICAL",
        "status": "IN_PROGRESS"
    }

    # Act
    put_response = api_request.put(
        f"/bugs/{bug_id}",
        headers=auth_headers,
        data=payload_atualizacao
    )

    print(f"Status Code do PUT: {put_response.status}")

    # Assert
    assert put_response.status == 200

    updated_bug = put_response.json()

    print("Response da API após atualização:")
    print(updated_bug)

    assert updated_bug["id"] == bug_id
    assert updated_bug["title"] == payload_atualizacao["title"]
    assert updated_bug["description"] == payload_atualizacao["description"]
    assert updated_bug["priority"] == payload_atualizacao["priority"]
    assert updated_bug["status"] == payload_atualizacao["status"]

    get_response = api_request.get(
        f"/bugs/{bug_id}",
        headers=auth_headers
    )

    print(f"Status Code do GET: {get_response.status}")

    assert get_response.status == 200

    bug_after_update = get_response.json()

    print("Response da API após o GET:")
    print(bug_after_update)

    assert bug_after_update["id"] == bug_id
    assert bug_after_update["title"] == payload_atualizacao["title"]
    assert bug_after_update["description"] == payload_atualizacao["description"]
    assert bug_after_update["priority"] == payload_atualizacao["priority"]
    assert bug_after_update["status"] == payload_atualizacao["status"]