from app import app
import argparse
import logging
from logging.handlers import RotatingFileHandler

def argsPars():
    parser = argparse.ArgumentParser(description='Wintventory web server')
    parser.add_argument('--host', type=str, default="localhost", help='DB host url.', metavar='')
    parser.add_argument('-p', '--port', type=int, default=5000, help='DB user.', metavar='')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = argsPars()
    formatter = "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(filename=app.config['LOG_FILE'], level=logging.DEBUG, format=formatter)
    log = logging.getLogger(app.config['LOG_FILE'])
    handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10000000, backupCount=5)
    log.addHandler(handler)
    app.run(debug=True,
            host=args.host,
            port=args.port,
            threaded=True)