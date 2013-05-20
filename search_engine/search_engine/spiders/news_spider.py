from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.exceptions import CloseSpider

from w3lib.html import replace_escape_chars, remove_tags


#to check 
import urlparse


from search_engine.dbtools import DbTool
base_url = "http://www.newyorker.com"

class NewsSpider(BaseSpider):
    name = "newyorker"
    allowed_domains = ["newyorker.com"]
    start_urls = [
        "http://www.newyorker.com",
    ]

             
    def __init__(self):
		dispatcher.connect(self.on_spider_closed, signals.spider_closed)
		self.db = DbTool('search_engine.sql')

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        curr_url = response.url
        txt = hxs.select('//body')
        if txt: 
            txt = remove_tags(txt.extract()[0])
            self.db.add_to_index(curr_url, txt)
            #for word in self.db.separate_words(txt): print word
		
        urls =  hxs.select('//a[contains(@href,".html")]/@href')
        if urls:
            urls = urls.extract()
            #self.db.commit()
            for url in urls: 
                if url.find("'")!=-1 : continue
                url=url.split('#')[0]
                if url[0:4] !='http': 
                    url = '%s%s'%(base_url, url)
                if urlparse.urlsplit(url)[1].split(':')[0].startswith('www.newyorker.com'):
                    link_text = remove_tags(url)
                    self.db.add_link_ref(curr_url, url, link_text)                
                    yield Request(url, self.parse)                        
            

    
                
    def on_spider_closed(self):
        self.db.commit()
                
