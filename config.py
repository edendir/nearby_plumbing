import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ENV = os.environ.get('ENV', 'development')
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    MAIL_FROM = os.environ.get('MAIL_FROM')
    MAIL_TO = os.environ.get('MAIL_TO')