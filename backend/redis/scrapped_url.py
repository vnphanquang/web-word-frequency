from time import strftime
from redis_om import (Field, HashModel)

class ScrapedUrl(HashModel):
	ttl: int = Field(default=604740) # a week in seconds minus 60s to make sure expires before WebWordFrequency
	web_word_frequency_id: str = Field(index=True)
	url_sentence: str = Field(index=True, full_text_search=True)
	url: str = Field(index=False)
	scraped_at: str = Field(index=True, default=strftime("%Y-%m-%d %H:%M:%S"))