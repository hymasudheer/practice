from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider 

import datetime
import os
import csv

class Timetravels(BaseSpider):
	name = "romantic"
	start_urls = ['https://timesofindia.indiatimes.com/travel/romantic-places']
	
	def __init__(self):
		self.filename = "romanticplaces%s.csv" % (str(datetime.datetime.now().date()))
		self.csv_file = self.is_path_file_name(self.filename)
		self.fields = ["title", "tags"]
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
			'authority': 'timesofindia.indiatimes.com',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'en-US,en;q=0.9',
			#'cookie': '_col_uuid=10e9d50c-a17f-46ab-9e13-c1121fe72b03-10oth; __gads=ID=ef4c8140d5f52b58:T=1548410732:S=ALNI_MZFDRMHvHvPrqIKC6zLdqFYUBkaNw; _iibeat_session=edd64032-8d7b-45a6-9d23-f1420fddd1a1; ce_haptpd=aG9qd2NqZ3BqMWNqZ3BqaXF0aG9qd3UvZnFuQ3JiQzIyODY5OzcyOzI6OjM0QHYw; GED_PLAYLIST_ACTIVITY=W3sidSI6IitZcC8iLCJ0c2wiOjE1NDg4NTE4MjMsIm52IjoxLCJ1cHQiOjE1NDg4NTE4MTIsImx0IjoxNTQ4ODUxODIxfV0.; _ga=GA1.2.395131892.1549019465; geo_continent=AS; _fbp=fb.1.1549274701970.949427310',
		}
		
		yield Request('https://timesofindia.indiatimes.com/travel/romantic-places', headers=headers, callback = self.parse_next)
	
	def parse_next(self, response):
		page_no = sel.xpath('//div[@class="pagination2"]//a[contains(@class, "number-btn index")]/text()').extract()
		sel = Selector(response)
		import pdb;pdb.set_trace()
		for i in page_no:
			complete_url = 'https://timesofindia.indiatimes.com/travel/travel_destination.cms?curpg='+str(i)+'&ajax=1&query=mData_GuideGenre:%22romantic%22'
			#import pdb;pdb.set_trace()
			yield Request(complete_url, callback=self.parse_last)
		
	def parse_last(self, response):
		
		sel = Selector(response)
		nodes = sel.xpath('//div[@id="content_wrapper"]//div[contains(@class, "box1 one-third")]')
		for node in nodes:
			title = (''.join(node.xpath('.//h3/a/text()').extract()).replace('\n', '')).encode("utf-8")
			tags = ','.join(node.xpath('.//p[@class="toggle tags"]//a/text()').extract())
			csv_values = [title, tags]
			self.csv_file.writerow(csv_values)
			#import pdb;pdb.set_trace()		
