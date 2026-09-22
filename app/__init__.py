from flask import Flask, jsonify

from flask_sqlalchemy import SQLAlchemy

from flasgger import Swagger

from flask_jwt_extended import JWTManager

from werkzeug.security import generate_password_hash


db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    # ==========================================
    # Configuração do banco de dados
    # ==========================================

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bug_tracking.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ==========================================
    # Configuração do JWT
    # ==========================================

    app.config["JWT_SECRET_KEY"] = "chave-secreta-do-projeto"

    # ==========================================
    # Inicialização das extensões
    # ==========================================

    db.init_app(app)

    jwt = JWTManager(app)

    # ==========================================
    # Mensagens de erro do JWT em português
    # ==========================================

    @jwt.unauthorized_loader
    def unauthorized_callback(error):

        return jsonify({
            "message": "Token de autenticação não informado"
        }), 401


    @jwt.invalid_token_loader
    def invalid_token_callback(error):

        return jsonify({
            "message": "Token de autenticação inválido"
        }), 401


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):

        return jsonify({
            "message": "Token de autenticação expirado"
        }), 401


    # ==========================================
    # Configuração do Swagger / OpenAPI 3
    # ==========================================

    swagger_config = {

        "headers": [],

        "title": "Bug API",

        "openapi": "3.0.2",

        "specs": [
            {
                "endpoint": "apispec",

                "route": "/apispec.json",

                "rule_filter": lambda rule: True,

                "model_filter": lambda tag: True,
            }
        ],

        "static_url_path": "/flasgger_static",

        "swagger_ui": True,

        "specs_route": "/apidocs/",
    }


    swagger_template = {

        "openapi": "3.0.2",

        "info": {

            "title": "Bug Tracking API",

            "description": "API para gerenciamento de bugs",

            "version": "1.0.0",
        },

        "components": {

            "securitySchemes": {

                "BearerAuth": {

                    "type": "http",

                    "scheme": "bearer",

                    "bearerFormat": "JWT",

                    "description": "Informe apenas o token JWT."
                }
            }
        },
    }


    Swagger(
        app,

        config=swagger_config,

        template=swagger_template
    )


    # ==========================================
    # Importação dos models
    # ==========================================

    from app.models.bug import Bug

    from app.models.user import User


    # ==========================================
    # Criação das tabelas e usuário inicial
    # ==========================================

    with app.app_context():

        db.create_all()

        user = User.query.filter_by(
            email="qa@example.com"
        ).first()


        if not user:

            user = User(

                name="QA Tester",

                email="qa@example.com",

                password_hash=generate_password_hash("123456")
            )

            db.session.add(user)

            db.session.commit()


    # ==========================================
    # Registro das rotas
    # ==========================================

    from app.routes import api

    app.register_blueprint(api)


    return app