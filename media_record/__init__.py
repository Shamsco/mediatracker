from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    from media_record.db import db_session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    from media_record.auth import auth
    app.register_blueprint(auth.blp)

    from media_record.records import records
    app.register_blueprint(records.blp)
    print(app.url_map)
    return app