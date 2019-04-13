# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem


class TencentpostionSpider(scrapy.Spider):
	"""
	功能：爬取腾讯社招信息
	"""
	# 爬虫名
	name = 'tencentPostion'
	# 爬虫作用范围
	allowed_domains = ['tencent.com']


	url = 'https://hr.tencent.com/position.php?&start='
	offset = 0
	# 起始url
	start_urls = [url + str(offset)]

	def parse(self, response):
		for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
			# 初始化模型对象
			item = TencentItem()

			item['positionname'] = each.xpath("./td[1]/a/text()").extract()[0]
			item['positionlink'] = each.xpath("./td[1]/a/@href").extract()[0]
			if len(each.xpath("./td[2]/text()").extract()) > 0:
				item['positionType'] = each.xpath('./td[2]/text()').extract()[0]
			else:
				item['positionType'] = "None"
			item['peopleNum'] = each.xpath("./td[3]/text()").extract()[0]
			item['workLocation'] = each.xpath("./td[4]/text()").extract()[0]
			item['publishTime'] = each.xpath("./td[5]/text()").extract()[0]

			yield item

		if self.offset < 2000:
			self.offset += 10

		# 每次处理完一页的数据之后，重新发送下一页页面请求
		# self.offset自增10，同时拼接为新的url，并调用回调函数self.parse处理Response
		yield scrapy.Request(self.url + str(self.offset), callback=self.parse, dont_filter=True)

