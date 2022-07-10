from redis_om import Migrator, FindQuery

from .web_word_frequency import *
from .scrapped_url import *

Migrator().run()