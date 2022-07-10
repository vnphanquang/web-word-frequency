from flask import request
from functools import wraps
from typing import List, Any

class Pagination(object):
	page: int
	per_page: int

	def __init__(self, page: int, per_page: int):
		self.page = page
		self.per_page = per_page

	def __iter__(self):
		for k,v in vars(self).items():
			yield k,v

	def start(self):
		return (self.page - 1) * self.per_page

	def end(self):
		return self.start() + self.per_page;

	def paginate(self, list: List[Any]):
		return list[self.start():self.end()]

def pagination_query_params(f):
	@wraps(f)
	def logic():
		page = request.args.get('page', default=1, type=int)
		page = 0 if page < 0 else page
		per_page = request.args.get('per_page', default=10, type=int)
		per_page = 1 if per_page < 1 else per_page
		return f(pagination=Pagination(page, per_page))
	return logic

