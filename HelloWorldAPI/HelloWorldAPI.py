import logging
from argparse import ArgumentParser

from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from helloWordController import hello_controller

LOG = logging.getLogger(__name__)

if __name__ == '__main__':
    # Parse application arguments
    arg_parser = ArgumentParser(description="My Rames Server")
    arg_parser.add_argument('-c', '--config', help="Configuration file location (default: ./config.py)",
                        metavar='<configuration file>', type=str, default='./config.py')
    arg_parser.add_argument('-s', '--static-folder', help="Static resource folder path (default: ./static)",
                        metavar='<static folder path>', type=str, default='./static')
    arg_parser.add_argument('-l', '--log-level', help="Level of logger", metavar='<logging level>', type=str,
                        default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'FATAL'])
    args = arg_parser.parse_args()

    # Create and configure apps
    app: Flask = Flask(__name__, static_url_path='/app', static_folder=args.static_folder)
    app.config.from_pyfile(args.config)
    app.config['LOG_LEVEL'] = args.log_level

    # Proxy settings
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    # CORS setup for Flask
    if app.config.get('ENABLE_CORS', False):
        app.logger.warning("ENABLE CORS")
        cors = CORS(app, resources={r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000", "moz-extension://*"],
            "supports_credentials": True
        }})

    # Blueprints
    app.register_blueprint(hello_controller)

    # Start server
    host = app.config.get('SERVER_HOST', '127.0.0.1')
    port = app.config.get('SERVER_PORT', 5000)
    debug = app.config.get('DEBUG', False)
    app.logger.info("Start Flask-socketio server on host {} and port {}".format(host, port))
    if debug:
        app.logger.warning('DEBUG mode enabled')
        sql_logger = logging.getLogger('sqlalchemy.engine')
        sql_logger.setLevel(logging.DEBUG)
    app.run(host=host, port=port, debug=debug)
