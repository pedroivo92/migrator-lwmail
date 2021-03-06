from flask import Flask, request, make_response, jsonify
from flask_expects_json import expects_json
from jsonschema import ValidationError
import logging

from schema import *
from migration_service import *


logging.basicConfig(level=logging.INFO, filename='api.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def create_app():
    app = Flask(__name__)
    app.debug = True

    @app.route("/migration", methods=["POST"])
    @expects_json(schema_migration)
    def migration_handler():
        try:
            logging.info("API: Receiving Request for email migrations")
            migration_service = MigrationHandler(request.json)
            return migration_service.migration_handler()
        except Exception as e:
            logging.error(f"API: An error ocurred - {e}")
            return f"An error ocurred - {e}", HTTPStatus.BAD_REQUEST.value


    @app.route("/migration_status", methods=["POST"])
    @expects_json(schema_migration_status)
    def migration_status():
        try:
            logging.info("API: Receiving Request for email migration status")
            migration_service = MigrationHandler(request.json)
            return migration_service.migration_status()
        except Exception as e:
            return f"An error ocurred - {e}", HTTPStatus.BAD_REQUEST.value
    
    @app.route("/v2/migration-status", methods=["POST"])
    @expects_json(schema_migration_status)
    def migration_status_v2():
        try:
            logging.info("API: Receiving Request for email migration status v2")
            migration_service = MigrationHandler(request.json)
            return migration_service.migration_status_v2()
        except Exception as e:
            return f"An error ocurred - {e}", HTTPStatus.BAD_REQUEST.value
    
    @app.route("/reprocess", methods=["POST"])
    @expects_json(schema_migration_status)
    def reprocess():
        try:
            logging.info("API: Reprocess registry")
            migration_service = MigrationHandler(request.json)
            return migration_service.reprocess()
        except Exception as e:
            return f"An error ocurred - {e}", HTTPStatus.BAD_REQUEST.value
    
    @app.route("/reprocess-migration", methods=["POST"])
    @expects_json(schema_migration_status)
    def reprocess_migration():
        try:
            logging.info("API: Reprocess migration registry")
            migration_service = MigrationHandler(request.json)
            return migration_service.reprocess_migration()
        except Exception as e:
            return f"An error ocurred - {e}", HTTPStatus.BAD_REQUEST.value
    
    @app.route("/statistics", methods=["GET"])
    def statistics():
        try:
            logging.info("API: getting statistics")

            migration_service = MigrationHandler()
            return migration_service.statitics()
        except Exception as e:
            return f"An error ocurred - {e}", HTTPStatus.BAD_REQUEST.value
    
    @app.route("/submit-banner", methods=["POST"])
    @expects_json(schema_banner)
    def submit_banner():
        try:
            logging.info("API: Receiving Banner information")
            migration_service = MigrationHandler(request.json)
            return migration_service.submit_banner()
        except Exception as e:
            return f"An error ocurred - {e}", HTTPStatus.BAD_REQUEST.value

    @app.route("/banner-historic", methods=["POST"])
    @expects_json(schema_migration_status)
    def banner_status():
        try:
            logging.info("API: Receiving Request for banner historic")
            migration_service = MigrationHandler(request.json)
            return migration_service.banner_historic()
        except Exception as e:
            return f"An error ocurred - {e}", HTTPStatus.BAD_REQUEST.value

    @app.errorhandler(400)
    def bad_request(error):
        if isinstance(error.description, ValidationError):
            original_error = error.description
            return make_response(jsonify({'error': original_error.message}), 400)

        return error

    return app