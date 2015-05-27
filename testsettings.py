import django

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

if django.VERSION < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'

if django.VERSION >= (1, 7):
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware'
    )
