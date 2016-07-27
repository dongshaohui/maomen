#coding=utf-8
"""
Django settings for maomen project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o$#3y#2g5s-t9ajt$7_(k305zt#6#jz8*jw!nd8(u)sf@lmnql'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'broadcast',
    'gunicorn',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'maomen.urls'

WSGI_APPLICATION = 'maomen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'maomen_test', # 测试
        # 'NAME': 'mifan_qingdao', #生产
        'USER': 'dongshaohui',
        'PASSWORD': 'Dsh5561225',
        'HOST': 'rm-2ze326p1v5k528e1ro.mysql.rds.aliyuncs.com',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': True,
#     'formatters': {
#         'standard': {
#                 'format': '[%(name)s:%(lineno)d] [%(levelname)s]- [%(asctime)s] %(message)s'
#                 },
#     },
#     'filters': {
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'formatter':'standard',
#         },
#         'default': {
#             'level':'INFO',
#             'class':'logging.handlers.RotatingFileHandler',
#             'filename':os.path.join('/home/maomen_log'+'/logs/','default.log'), 
#             'formatter':'standard',
#         },
#         'user': {
#             'level':'INFO',
#             'class':'logging.handlers.RotatingFileHandler',
#             'filename':os.path.join('/home/maomen_log'+'/logs/','user.log'), 
#             'formatter':'standard',
#         },     
#         'record': {
#             'level':'INFO',
#             'class':'logging.handlers.RotatingFileHandler',
#             'filename':os.path.join('/home/maomen_log'+'/logs/','record.log'), 
#             'formatter':'standard',
#         },            
#         'test2_handler': {
#             'level':'DEBUG',
#                    'class':'logging.handlers.RotatingFileHandler',
#             'filename':'path2',
#             'formatter':'standard',
#         },
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'default':{
#             'handlers': ['default'],
#             'level': 'INFO',
#             'propagate': True
#         },
#         'user':{
#             'handlers': ['user'],
#             'level': 'INFO',
#             'propagate': True
#         },    
#         'record':{
#             'handlers': ['record'],
#             'level': 'INFO',
#             'propagate': True
#         },                
#          'test2':{
#             'handlers': ['test2_handler'],
#             'level': 'INFO',
#             'propagate': False
#         },
#     }
# }