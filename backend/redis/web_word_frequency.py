from redis_om import (Field, JsonModel)
from typing import List, Tuple
from time import strftime

class WebWordFrequency(JsonModel):
	encoded_url: str = Field(index=True)
	ttl: int = Field(default=604800,index=False) # a week in seconds
	url: str = Field(index=False)
	process_time: float = Field(index=False)
	total: int = Field(index=False)
	words: List[Tuple[str, int]] = Field(index=False)
	scraped_at: str = Field(index=True, default=strftime("%Y-%m-%d %H:%M:%S"))
