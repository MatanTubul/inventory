from flask_mail import Mail
from app import app

app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='invenotrymail@gmail.com',
    MAIL_PASSWORD='i03b04wint'
)
mail = Mail(app)
