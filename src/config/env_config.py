from starlette.config import Config

try:
    config = Config('.env')

except FileNotFoundError:
    config = Config()



MONGODB_URI = config("MONGODB_URI" , cast=str)