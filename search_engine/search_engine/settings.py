# Scrapy settings for search_engine project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'search_engine'

SPIDER_MODULES = ['search_engine.spiders']
NEWSPIDER_MODULE = 'search_engine.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'search_engine (+http://www.yourdomain.com)'


#LOG_ENABLED = False
CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_IP = 8
