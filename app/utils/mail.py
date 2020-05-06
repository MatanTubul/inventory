from flask_mail import Mail
from app import app

app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='mail',
    MAIL_PASSWORD='password'
)
mail = Mail(app)
