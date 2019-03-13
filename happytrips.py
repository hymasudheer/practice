from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider 
j = 0
class Happytrips(BaseSpider):
	name = "trips"
	start_urls = ['https://timesofindia.indiatimes.com/travel/destinations']
	#start_urls = ['https://timesofindia.indiatimes.com/travel/romantic-places']
		
	def parse(self, response):
		reference = response.url
		sel = Selector(response)
		des = ['romantic', 'historical', 'religious', 'beaches', 'city', 'hill+stations', 'adventure', 'wildlife']
		for i in des:
			url = 'https://timesofindia.indiatimes.com/travel/travel_destination.cms?curpg=1&ajax=1&query=mData_GuideGenre:%22'+i+'%22'
			import pdb;pdb.set_trace()
			yield Request(url, callback = self.parse_data, meta = {'des':des, 'url':url})
					
	def parse_data(self, response):
		sel = Selector(response)
		reference = response.url
		des = response.meta['des']
		# write xpaths for page numbers and take in list
		for i in range(1, 7):
			complete_url = 'https://timesofindia.indiatimes.com/travel/travel_destination.cms?curpg='+str(i)+'&ajax=1&query=mData_GuideGenre:%22'+des[j]+'%22'
			yield Request(complete_url, callback=self.parse_next, meta={'reference':reference, 'complete_url':complete_url})
		
	def parse_next(self, response):
		sel = Selector(response)
		nodes = sel.xpath('//div[@id="content_wrapper"]//div[contains(@class, "box1 one-third")]')
		for node in nodes:
			title = (''.join(node.xpath('.//h3/a/text()').extract()).replace('\n', '')).encode("utf-8")
			tags = ','.join(node.xpath('.//p[@class="toggle tags"]//a/text()').extract())
			#print (title)
		yield Request(response.url, callback=self.parse)
		#import pdb;pdb.set_trace()
	
'''		
	
	
	
	def parse(self, response):
		sel = Selector(response)
		#index = sel.xpath('//div[@class="pagination2"]//a[@class="next"]/@lastindex').extract()
		node = sel.xpath('//div[@class="clearfix tab_data"]//li/a')
		for x in node:
			destination_link = ''.join(x.xpath('./@href').extract())
			yield Request(destination_link, callback = self.parse_next)

	def parse_next(self, response):
		sel = Selector(response)
		nodes = sel.xpath('//div[@id="content_wrapper"]//div[@itemtype="https://schema.org/ImageObject"]')
		for node in nodes:
			title = (''.join(node.xpath('.//h3/a/text()').extract()).replace('\n', '')).encode("utf-8")
			tags = ','.join(node.xpath('.//p[@class="toggle tags"]//a/text()').extract())
			#import pdb;pdb.set_trace()'''
'''	def parse_next(self, response):
		sel = Selector(response)
		nodes = sel.xpath('//div[@id="content_wrapper"]//div[@itemtype="https://schema.org/ImageObject"]')
		for node in nodes:
			title = (''.join(node.xpath('.//h3/a/text()').extract())).replace('\n', '')
			tags = ','.join(node.xpath('.//p[@class="toggle tags"]//a/text()').extract())
			link = ''.join(node.xpath('.//h3/a/@href').extract())
			page_link = 'https://timesofindia.indiatimes.com' + link
		#index = ''.join(sel.xpath('//div[@class="pagination2"]//a[@class="next"]/@lastindex').extract())
		link = sel.xpath('//div[@class="pagination2"]//a')
		for x in link:
			page = ''.join(x.xpath('./@href').extract())
			full_link = 'https://timesofindia.indiatimes.com' + page
			if full_link:  tried for next page urls code'''
			
'''	'for next in next_page:
			next_link = next.xpath('.//@href').extract()
			import pdb;pdb.set_trace()
		nodes = sel.xpath('//div[@id="content_wrapper"]//div[@class="box1 one-third"]')
		for node in nodes:
			tags = ''.join(node.xpath('.//p[@class="toggle tags"]/a/text()').extract())
			title = ''.join(node.xpath('.//h3/a/text()').extract())
			link = ''.join(node.xpath('.//h3/a/@href').extract())
			#print (tags)'''
			