from requests import get
from bs4 import BeautifulSoup
import re
from collections import defaultdict
from typing import List, Tuple

def get_text_from_url(url: str):
	page = get(url)
	soup = BeautifulSoup(page.content, features="html.parser")
	return soup.get_text()

def count_word_frequencies(text: str, sort = True) -> List[Tuple[str, int]]:
	words = re.findall(r'\b[a-zA-Z-\-]+\b', text)
	frequencies = defaultdict(int)
	for word in words:
		match = re.match(r'\w+', word)
		if bool(match):
			normalized = word.lower()
			frequencies[normalized] += 1
	if sort:
		frequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
	else:
		frequencies = frequencies.items()
	return frequencies

def url_to_sentence(url: str) -> str:
	words = re.findall(r'\w+', url)
	return ' '.join(words)