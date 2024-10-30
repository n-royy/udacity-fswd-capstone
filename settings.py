from dotenv import load_dotenv
import os
load_dotenv()

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = os.environ.get("ALGORITHMS")
API_AUDIENCE = os.environ.get("API_AUDIENCE")
DATABASE_PATH = os.environ.get("DATABASE_PATH")
DATABASE_PATH_TEST = os.environ.get("DATABASE_PATH_TEST")
ASSISTANT_TOKEN = os.environ.get('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.environ.get('DIRECTOR_TOKEN')
