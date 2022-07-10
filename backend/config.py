import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, ".env"))

class Config(object):
	MODE = os.environ.get("MODE")
	PORT = os.environ.get("PORT")