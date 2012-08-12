# Django settings for codecollision project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('hexvector', 'michael@hexvector.net'),
)

MANAGERS = ADMINS

APPEND_SLASH = True

CACHE_MIDDLEWARE_SECONDS = 3600
CACHE_MIDDLEWARE_KEY_PREFIX = ''

DATABASES = {

    # flash version database
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hexvector_log_wp',
        'USER': 'hexvector_log_wp',
        'PASSWORD': '&Mdolcs&xgjB',
        'HOST': '',
        'PORT': '',
    },
    'django': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hexvector_django',
        'USER': 'hexvector_django',
        'PASSWORD': 'jusnwIOWNII15483&^%@)',
        'HOST': '',
        'PORT': '',
    },
    # html version database
    'blog': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hexvector_blog_w',
        'USER': 'hexvector_blog_w',
        'PASSWORD': 'DsmoIL9G8e1M',
        'HOST': '',
        'PORT': '3306',
    }
}

DATABASE_ROUTERS = ['codecollision.dbrouter.dbrouter', ]


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Phoenix'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/hexvector/webapps/codecollision_media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://dtli0f3gwjwjm.cloudfront.net/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/hexvector/webapps/codecollision_media/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'e462%cs=&)=^%rg08_fv=zontk44j8m7v=@vf+0q03j5r-!k$2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    #'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
)

ROOT_URLCONF = 'codecollision.urls'

TEMPLATE_DIRS = (
    '/home/hexvector/webapps/django2/codecollision/polls/templates',
    '/home/hexvector/webapps/django2/codecollision/wp/templates',
    '/home/hexvector/webapps/django2/codecollision/log/templates',
)

INSTALLED_APPS = (
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.messages',
    #'django.contrib.staticfiles',
    'codecollision.log',
    #'django.contrib.admin',
    # 'django.contrib.admindocs',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'codecollision'
    }
}