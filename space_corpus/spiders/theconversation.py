import os
import scrapy

cookies = {
	"_dd_s": "rum=0&expire=1641209179228",
	"tc_region": "uk",
	"tc_session": "R1ZpQVhldzB2NFNubTRWSkFBRWJZRzdwQ0pZZDR1L0xFSk9kaXRZYXJMQnJuMXRueEZUMlJKT1ZSZWNGWUJ3aDAySGZMY0JOZFhTb09tcElqazNWSko3QW1laEt4WWd3enJ6VFd2RjJJdWdOcitBckVIQWdudUZQMEU2eWlvMmtDTUlibHBYMTM1cVdQY1FUcmVleGQza3ZpNTkremxoeHdOK285Z0wwQ3dxY2tZZUNZNUw5ZzdyK2JYZ2VVWGhvVitDNlNCRUpBOUE1N1FmYXVvVjNVSC94eHFLV1NZOE43OUlIcmJQYUtlRVdkclhoTjkwU1JabzM3MmRlUFptWnJzRmxzVmQ0SFJiazZyc3UzYmFKd05SdHMxUU9KeFpySm1NSGZOT0dqV0E9LS1YWkFRVFV0bjlrRmJpYmNZNGUwM05BPT0=--08d78fa9c345110327d70ef42bb5eb050a36fa58"
}

class TheconversationSpider(scrapy.Spider):
	name = 'theconversation'
	allowed_domains = ['theconversation.com']

	def start_requests(self):
		with open(os.path.join('urls', 'theconversation_fr.txt')) as fp:
			urls = fp.readlines()

		for url in urls:
			yield scrapy.Request(url=url.strip(), cookies=cookies, callback=self.parse)

	def parse(self, response):
		article_links = response.xpath("//section[@id='articles']//article/header/div/h2/a")
		next = response.xpath("//span[@class='next']/a")

		yield from response.follow_all(article_links, callback=self.parse_article)

		if next:
			yield response.follow(next[0], callback=self.parse)

	def parse_article(self, response):
		# title
		title = response.xpath("//article//header//h1//text()").extract()
		title = ''.join(title).strip().replace(u'\xa0', u' ')

		# authors
		authors = response.xpath("//*[@itemprop='author']/a/@href").extract()

		# topics
		topics = response.xpath("//li[@class='topic-list-item']/a")
		topics = list(map(lambda a: a.xpath('text()').extract() + a.xpath('@href').extract(), topics))

		# content
		elements = response.xpath("//div[@itemprop='articleBody']/p | //div[@itemprop='articleBody']/h2 | //div[@itemprop='articleBody']/blockquote")
		full_text = title + '\n\n'

		for element in elements:
			text = ''.join(element.xpath('.//text()').extract())

			if text.strip().startswith('Read more:') or text.strip().startswith('À lire aussi:') :
				continue

			if element.root.tag == 'h2':
				full_text += '\n' + text + '\n\n'
			else:
				full_text += text + '\n'

		yield {
			"title": title,
			"text": full_text,
			"authors": authors,
			"topics": topics,
			"url": response.url
		}

