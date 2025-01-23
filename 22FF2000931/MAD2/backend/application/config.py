class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'mysecretkey'
    SECURITY_TRACKABLE = True    
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'

    MAIL_SERVER = 'localhost' # '127.0.0.1'
    MAIL_PORT = 1025
    MAIL_DEFAULT_SENDER = 'no-reply@a.com'

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'localhost' # '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_DEFAULT_TIMEOUT = 60 # caching it for 1 min/ 60 sec  


    DEBUG = True

