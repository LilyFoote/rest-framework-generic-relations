DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',

    'generic_relations',
    'generic_relations.tests',
)

ROOT_URLCONF = ''

SECRET_KEY = 'abcde12345'
