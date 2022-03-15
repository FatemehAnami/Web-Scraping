"""
This program is used for reading data from given URLs and save articles into .txt files.
For loading and reading URLs we use Scrapy library. 
"""

import scrapy
import pandas as pd 
import datetime as dt
import sys

def main():
    spider = ArticlesUrlsSpider()

    
class ArticlesUrlsSpider(scrapy.Spider):
    name = 'articles_urls'

    def start_requests(self):
        df = pd.read_excel('Input.xlsx')
        for i in range(len(df)):
            url = df['URL'][i]
            url_id = df['URL_ID'][i]

            yield scrapy.Request(url=url, dont_filter=True, meta = {'url_id' : url_id}) 

    def parse(self, response):
        # Extracting the content using css selectors
        title = response.css('title::text').extract()
        body = response.css('p::text').extract()
        scraped_info= str(title) + str(body)
        name = response.meta['url_id']
        filename = f'{name}.txt'
        with open(filename, 'xt', encoding='UTF-8', errors='ignore') as file:
            file.write(scraped_info)
        

if __name__ == '__main__':
    start = dt.datetime.now()
    print(f'\n\n{start.strftime("%c")}\nPROGRAM NAME: {sys.argv[0]}\n')
    main()
    print(f'\n\nRuntime: {(dt.datetime.now()-start)}')
    print(f'\nNormal termination.\n{dt.datetime.now().strftime("%c")}\n')