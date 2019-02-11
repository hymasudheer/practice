from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider

import json
import datetime
import os
import csv

class zeemovies(BaseSpider):
	name = "zeemovies"
	start_urls = ['https://www.zee5.com/movies/all']
	
	def __init__(self):
		self.filename = "zeemovies%s.csv" % (str(datetime.datetime.now().date()))
		self.csv_file = self.is_path_file_name(self.filename)
		self.fields = ["movie_list"]
		self.csv_file.writerow(self.fields)
		
	def is_path_file_name(self, excel_file_name):
		if os.path.isfile(excel_file_name):
			os.system('rm%s' % excel_file_name)
		oupf = open(excel_file_name, 'ab+')
		todays_excel_file = csv.writer(oupf)
		return todays_excel_file
		
	
	def parse(self, response):
		reference = response.url
		
		headers = {
			'X-Z5-Appversion': '14.18.1',
			'Accept': 'application/json, text/plain, */*',
			'Referer': 'https://www.zee5.com/movies/all',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
			'X-Z5-AppPlatform': 'Web Desktop',
		}

		yield Request('https://catalogapi.zee5.com/v1/movie?asset_subtype=movie&sort_by_field=release_date&sort_order=DESC&page=1&page_size=24&genres=Action,Awards,Animation,Crime,Fantasy,Horror,Music,Mystery,Patriotic,Thriller,Romance,Devotional,Entertainment,News,Drama,Sports,Docudrama,Cookery,Comedy&languages=hi,en,mr,te,kn,ta,ml,bn,gu,pa,hr,or&country=IN&translation=en', callback = self.parse_next, headers=headers)
		
	def parse_next(self, response):
		info = json.loads(response.body)
		total = info.get('total','')
		for i in range(1, 114):
			complete_url = 'https://catalogapi.zee5.com/v1/movie?asset_subtype=movie&sort_by_field=release_date&sort_order=DESC&page='+str(i)+'&page_size=24&genres=Action,Awards,Animation,Crime,Fantasy,Horror,Music,Mystery,Patriotic,Thriller,Romance,Devotional,Entertainment,News,Drama,Sports,Docudrama,Cookery,Comedy&languages=hi,en,mr,te,kn,ta,ml,bn,gu,pa,hr,or&country=IN&translation=en'
			yield Request(complete_url, callback=self.parse_last)
			#import pdb;pdb.set_trace()
	
	def parse_last(self, response):
		data = json.loads(response.body)
		item = data.get('items','')
		for x in item:
			movie_name = x.get('title', '')
			csv_values = [movie_name]
			self.csv_file.writerow(csv_values)
			#print(title)
			#import pdb;pdb.set_trace()
		