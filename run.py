from app import app
import argparse

def argsPars():
    parser = argparse.ArgumentParser(description='Wintventory web server')
    parser.add_argument('--host', type=str, default="localhost", help='DB host url.', metavar='')
    parser.add_argument('-p', '--port', type=int, default=5000, help='DB user.', metavar='')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = argsPars()
    app.run(debug=True,
            host=args.host,
            port=args.port)