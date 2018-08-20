DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'skilltrade',
        'USER': 'root',
        'PASSWORD': 'not2secret!ml',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

MEDIA_ROOT='/Users/stefan/Dev/projects/skilltrade/media'
MEDIA_URL='/media/'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'TODO DEFAULT EMAIL <todo@todo.com>'
