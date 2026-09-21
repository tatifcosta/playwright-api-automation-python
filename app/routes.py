from flask import Blueprint, jsonify, request

from app import db

from app.models.bug import Bug
from app.models.user import User

from werkzeug.security import check_password_hash

from flask_jwt_extended import create_access_token, jwt_required


api = Blueprint("api", __name__)


# =========================================================
# HEALTH CHECK
# =========================================================

@api.get("/health")
def health():
    """
    Verificar disponibilidade da API
    ---
    tags:
      - Health Check
    responses:
      200:
        description: API está ativa e funcionando
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: UP
                message:
                  type: string
                  example: Bug Tracking API está ativa e funcionando
    """

    return jsonify({
        "status": "UP",
        "message": "Bug Tracking API está ativa e funcionando"
    }), 200


# =========================================================
# LOGIN
# =========================================================

@api.post("/auth/login")
def login():
    """
    Realizar login
    ---
    tags:
      - Autenticação
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - email
              - password
            properties:
              email:
                type: string
                example: qa@example.com
              password:
                type: string
                example: "123456"
    responses:
      200:
        description: Login realizado com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
                  example: eyJhbGciOiJIUzI1NiIs...
      400:
        description: Corpo da requisição inválido
      401:
        description: Email ou senha inválidos
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "message": "O corpo da requisição deve ser um JSON válido"
        }), 400

    if "email" not in data or "password" not in data:
        return jsonify({
            "message": "Email e senha são obrigatórios"
        }), 400

    user = User.query.filter_by(
        email=data["email"]
    ).first()

    if not user or not check_password_hash(
        user.password_hash,
        data["password"]
    ):
        return jsonify({
            "message": "Email ou senha inválidos"
        }), 401

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "access_token": access_token
    }), 200


# =========================================================
# CRIAR BUG
# =========================================================

@api.post("/bugs")
@jwt_required()
def create_bug():
    """
    Criar um novo bug
    ---
    tags:
      - Bugs
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - title
              - description
              - priority
              - status
            properties:
              title:
                type: string
                example: Botão de login não funciona
              description:
                type: string
                example: Ao clicar no botão, nada acontece
              priority:
                type: string
                example: HIGH
              status:
                type: string
                example: OPEN
    responses:
      201:
        description: Bug criado com sucesso
      400:
        description: Dados inválidos
      401:
        description: Token de autenticação não informado ou inválido
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "message": "O corpo da requisição deve ser um JSON válido"
        }), 400

    required_fields = [
        "title",
        "description",
        "priority",
        "status"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "message": "Campos obrigatórios não informados",
            "fields": missing_fields
        }), 400

    bug = Bug(
        title=data["title"],
        description=data["description"],
        priority=data["priority"],
        status=data["status"]
    )

    db.session.add(bug)
    db.session.commit()

    return jsonify({
        "id": bug.id,
        "title": bug.title,
        "description": bug.description,
        "priority": bug.priority,
        "status": bug.status
    }), 201


# =========================================================
# LISTAR BUGS
# =========================================================

@api.get("/bugs")
@jwt_required()
def get_bugs():
    """
    Listar todos os bugs cadastrados
    ---
    tags:
      - Bugs
    security:
      - BearerAuth: []
    responses:
      200:
        description: Lista de todos os bugs cadastrados
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  title:
                    type: string
                    example: Botão de login não funciona
                  description:
                    type: string
                    example: Ao clicar no botão, nada acontece
                  priority:
                    type: string
                    example: HIGH
                  status:
                    type: string
                    example: OPEN
      401:
        description: Token de autenticação não informado ou inválido
    """

    bugs = Bug.query.all()

    return jsonify([
        {
            "id": bug.id,
            "title": bug.title,
            "description": bug.description,
            "priority": bug.priority,
            "status": bug.status
        }
        for bug in bugs
    ]), 200


# =========================================================
# BUSCAR BUG POR ID
# =========================================================

@api.get("/bugs/<int:bug_id>")
@jwt_required()
def get_bug_by_id(bug_id):
    """
    Consultar bug por ID
    ---
    tags:
      - Bugs
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: bug_id
        required: true
        schema:
          type: integer
        example: 1
    responses:
      200:
        description: Bug encontrado com sucesso
      401:
        description: Token de autenticação não informado ou inválido
      404:
        description: Bug não encontrado
    """

    bug = db.session.get(Bug, bug_id)

    if not bug:
        return jsonify({
            "message": "Bug não encontrado"
        }), 404

    return jsonify({
        "id": bug.id,
        "title": bug.title,
        "description": bug.description,
        "priority": bug.priority,
        "status": bug.status
    }), 200


# =========================================================
# ATUALIZAR BUG
# =========================================================

@api.put("/bugs/<int:bug_id>")
@jwt_required()
def update_bug(bug_id):
    """
    Atualizar um bug
    ---
    tags:
      - Bugs
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: bug_id
        required: true
        schema:
          type: integer
        example: 1
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - title
              - description
              - priority
              - status
            properties:
              title:
                type: string
                example: Botão de login não funciona
              description:
                type: string
                example: O botão continua sem responder após a atualização
              priority:
                type: string
                example: HIGH
              status:
                type: string
                example: IN_PROGRESS
    responses:
      200:
        description: Bug atualizado com sucesso
      400:
        description: Dados inválidos
      401:
        description: Token de autenticação não informado ou inválido
      404:
        description: Bug não encontrado
    """

    bug = db.session.get(Bug, bug_id)

    if not bug:
        return jsonify({
            "message": "Bug não encontrado"
        }), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "message": "O corpo da requisição deve ser um JSON válido"
        }), 400

    required_fields = [
        "title",
        "description",
        "priority",
        "status"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "message": "Campos obrigatórios não informados",
            "fields": missing_fields
        }), 400

    bug.title = data["title"]
    bug.description = data["description"]
    bug.priority = data["priority"]
    bug.status = data["status"]

    db.session.commit()

    return jsonify({
        "id": bug.id,
        "title": bug.title,
        "description": bug.description,
        "priority": bug.priority,
        "status": bug.status
    }), 200


# =========================================================
# EXCLUIR BUG
# =========================================================

@api.delete("/bugs/<int:bug_id>")
@jwt_required()
def delete_bug(bug_id):
    """
    Excluir um bug
    ---
    tags:
      - Bugs
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: bug_id
        required: true
        schema:
          type: integer
        example: 1
    responses:
      204:
        description: Bug excluído com sucesso
      401:
        description: Token de autenticação não informado ou inválido
      404:
        description: Bug não encontrado
    """

    bug = db.session.get(Bug, bug_id)

    if not bug:
        return jsonify({
            "message": "Bug não encontrado"
        }), 404

    db.session.delete(bug)
    db.session.commit()

    return "", 204