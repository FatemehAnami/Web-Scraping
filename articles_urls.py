"""
This program is used for reading data from given URLs and save articles into .txt files.
For loading and reading URLs we use Scrapy library. 
"""

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
import pandas as pd 
import datetime as dt
import sys

def main():
    
    spider = CrawlerProcess({
       # If you want to change Setting file you should put them here as Dict data type
       })
   spider.crawl(ArticlesUrlsSpider)
   spider.start() 
  
class ArticlesUrlsSpider(scrapy.Spider):
    name = 'articles_urls'

    def start_requests(self):
        df = pd.read_excel('Input.xlsx') # it is your excel file which has 2 columns IDs and URLs of sites.
        # Store IDs and URLs in 2 different lists
        for i in range(len(df)):
            url = df['URL'][i]
            url_id = df['URL_ID'][i]

            yield scrapy.Request(url=url, dont_filter=True, meta = {'url_id' : url_id}) 

    def parse(self, response):
        # Extracting the title and body using css selectors (based on my sites title store in <title> tag and body store in <p> tag)
        title = response.css('title::text').extract()
        body = response.css('p::text').extract()
        scraped_info= str(title) + str(body)
        # name of the .txt file should be ID of each URL
        name = response.meta['url_id']
        filename = f'Scrapedfile\{name}.txt'
        # create a file and save scrapped data in it.
        with open(filename, 'xt', encoding='UTF-8', errors='ignore') as file:
            file.write(scraped_info)        

if __name__ == '__main__':
    start = dt.datetime.now()
    print(f'\n\n{start.strftime("%c")}\nPROGRAM NAME: {sys.argv[0]}\n')
    main()
    print(f'\n\nRuntime: {(dt.datetime.now()-start)}')
    print(f'\nNormal termination.\n{dt.datetime.now().strftime("%c")}\n')
