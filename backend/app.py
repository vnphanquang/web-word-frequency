from typing import List
from flask import Flask, request
from urllib.parse import (quote, unquote)
from time import time
from flask_cors import CORS

from .config import Config
from .operations import (count_word_frequencies, get_text_from_url, url_to_sentence)
from .redis import (WebWordFrequency, ScrapedUrl, FindQuery)
from .pagination import (Pagination, pagination_query_params)

def create_app(config_class=Config):
	app = Flask(__name__)
	CORS(app)
	app.config.from_object(config_class)

	@app.route("/web-word-frequency/recent")
	def recent():
		cache = FindQuery(
			expressions=[],
			model=ScrapedUrl,
			limit=5,
			sort_fields=["-scraped_at"]
		).execute()
		urls = list(map(lambda i: i.url, cache))

		return {
			"urls": urls
		}

	@app.route("/web-word-frequency/search")
	@pagination_query_params
	def search(pagination: Pagination):
		# search query
		query = unquote(request.args.get('query', default="", type=str))
		query = url_to_sentence(query)

		urls: List[str] = []
		if len(query) > 0: 
			# cache = ScrapedUrl.find(ScrapedUrl.url_sentence % query).all()
			# https://github.com/redis/redis-om-python/issues/284
			# https://github.com/redis/redis-om-python/blob/main/aredis_om/model/model.py#L337
			cache = FindQuery(
				expressions=[ScrapedUrl.url_sentence % query] if len(query) > 0 else [],
				model=ScrapedUrl,
				offset=pagination.start(),
				limit=pagination.per_page
			).execute()
			urls = list(map(lambda i: i.url, cache))
		
		return {
			**dict(pagination),
			"query": query,
			"results": urls,
		}
		

	@app.route("/web-word-frequency/scrape")
	@pagination_query_params
	def scrape(pagination: Pagination):
		# url
		url = unquote(request.args.get('url', default="", type=str))
		if url.endswith('/'):
			url = url[:-1]
		encoded_url = quote(url, safe="")
		from_cache: bool = False
		total: int
		process_time: float
		scraped_at: str
		words: list[tuple[str, int]]

		try:
			cache = WebWordFrequency.find(WebWordFrequency.encoded_url == encoded_url).all()

			if len(cache) == 0:
				start_time = time()
				words = [] if url == "" else count_word_frequencies(get_text_from_url(url))
				end_time = time()

				total = len(words)
				process_time = end_time - start_time

				web_word_frequency = WebWordFrequency(
					encoded_url=encoded_url,
					total=total,
					url=url,
					words=words,
					process_time=process_time
				)
				web_word_frequency.save()
				web_word_frequency.expire(web_word_frequency.ttl)

				scraped_at = web_word_frequency.scraped_at

				scrapped_url = ScrapedUrl(
					web_word_frequency_id=web_word_frequency.pk,
					url=url,
					url_sentence=url_to_sentence(url)
				)
				scrapped_url.save()
				scrapped_url.expire(scrapped_url.ttl)
			else:
				result: WebWordFrequency = cache[0]
				from_cache = True
				total = result.total
				process_time = result.process_time
				words = result.words
				scraped_at = result.scraped_at
		except Exception as e:
			return {
				"error": str(e)
			}, 400
		else:
			return {
				**dict(pagination),
				"total": total,
				"url": url,
				"words": pagination.paginate(words),
				"process_time": process_time,
				"scraped_at": scraped_at,
				"from_cached": from_cache,
			}

	return app

