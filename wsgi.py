from run import app
"""
This module used by "gunicorn" WSGI HTTP server, in order to start winteventory app in ssl mode please use
the following command:

gunicorn -w3 --certfile=wintventory.wintego.pem --keyfile=wintventory.wintego.key.pem --bind 0.0.0.0:5000 --log-file wintventory.log --log-level DEBUG wsgi:app
"""
if __name__ == "__main__":
    app.run()