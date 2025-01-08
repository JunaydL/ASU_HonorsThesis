import scrapy
#from scrapy.linkextractors import SgmlLinkExtractor

# the following is the code for the spider that scrapes the data from all blogs on sponsor's website
#cmd to run code: scrapy runspider aokblogs_sources.py
class AokblogsSpider(scrapy.Spider):
    name = "blogs_source"
    allowed_domains = [""] #place any specific website domains you would like to specifically look for
    MAX_PAGES = 5
    start_urls = []
    for i in range(1, MAX_PAGES + 1):
        start_urls.append("..." + str(i)) #place website you want to scrape here

    custom_settings = {
        'FEEDS': { 'tmp/aokblogs_sources.txt': { 'format': 'csv',}}
    }

    #rules = (
      # Extract links from current page and call parse_item for each link
    # scrapy.spiders.Rule(SgmlLinkExtractor(allow=r"/"), callback="parse", follow=False),
    #)

    def parse(self, response):  

        urls = response.xpath('//h3[@class="elementor-post__title"]/child::a/@href').getall()
        urls = urls[3:]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_item)
            
    def parse_item(self, response):
        #title = response.css('.elementor-heading-title::text').extract()
        title = response.xpath('/html/body/div[2]/section/div/div[1]/div/div[1]/div/h1/text()').getall()
        #content = response.css('.elementor-widget-container::text').extract()
        html_content = response.xpath('/html/body/div[2]/section/div/div[1]/div/div[2]/div//text()').getall()
        content = [' '.join(str(x) for x in html_content)]
        iAuthor = content[0].find("About The Author")
        if (iAuthor != -1 ):
            content[0] = content[0][:iAuthor] 
        #author = response.css('.awpa-display-name::text').extract()
        author = response.xpath('/html/body/div[2]/section/div/div[1]/div/div[2]/div/div/div/div[2]/h4/a/text()').getall()
        
        #Give the extracted content row wise
        for item in zip(title, content, author):
            #create a dictionary to store the scraped info
            scraped_info = {
                '' : "Title: " + item[0] + "\nSource: "+ response.url + "\n\n"
            }

            #yield or give the scraped info to scrapy
            yield scraped_info
            
    def save():
        content = ''
        html_content =["1","2"]
        for x in html_content:
            if ( str(x).find("About the Authorx") == -1):
                content = content + ' ' + str(x)
            else:
                break