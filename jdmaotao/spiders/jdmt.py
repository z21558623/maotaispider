# -*- coding: utf-8 -*-
import scrapy
from jdmaotao.items import JdmaotaoItem
from jdmaotao.items import JdCommentItem
import pandas as pd
import re
import json
class JdmtSpider(scrapy.Spider):
    name = 'jdmt'
    page = 1
    start_urls = []
    allowed_domains = ['jd.com']
    for i in range(0,1):
        url = 'https://search.jd.com/Search?keyword=%E8%8C%85%E5%8F%B0&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&stock=1&page='+str(i)+'&s=1&click=0'
        start_urls.append(url)



    
    custom_settings = {
        'ITEM_PIPELINES': {
            'jdmaotao.pipelines.JdmaotaoPipeline': 400
        }
    }
        
        
    def parse(self, response):
#        response.xpath('/div[@class="p-price"]/strong/i/text()').extract()
    # 处理每条留言

        for quote in response.xpath('//li[@class="gl-item"]'):
            item = JdmaotaoItem()
            item['price'] = quote.xpath('div/div[@class="p-price"]/strong/i/text()').extract_first()
            item['name'] = quote.xpath('div/div[contains(@class,"p-name")]/a/@title').extract_first()
            item['shopname'] = quote.xpath('div/div[@class="p-shop"]/span/a/text()').extract_first()
            item['commit'] = quote.xpath('div/div[@class="p-commit"]/strong/a/text()').extract_first()
            item['url'] = quote.xpath('div/div[@class="p-name p-name-type-2"]/a/@href').extract_first()
            item['productID']  = re.sub("\D", "", item['url'])#评论
            item['info']=[]
#            commentURL = 'https://sclub.jd.com/comment/productPageComments.action?productId='+re.sub("\D", "", item['url'])+'&score=0&sortType=3&page=1&pageSize=10'
#            yield scrapy.Request(commentURL, callback=self.info_parse, meta={"item": item})

            starsURL = 'https://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds='+re.sub("\D", "", item['url'])
#            starsURL = 'https://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds=7814515'
#            starsURL = 'https://club.jd.com/clubservice.aspx?method=GetCommentsCount&referenceIds='+'4352869'

            yield scrapy.Request(starsURL, callback=self.stars_parse, meta={"item": item})
            
      
    


# =============================================================================
#     def info_parse(self, response):
#         """
#         链接跟进，爬取每件商品的详细信息,所有的信息都保存在item的一个子字段info中
#         :param response:
#         :return:
#         """
#         body = response.body
# #        try:
# #            bjson=json.loads(body.decode('gbk'))
# #            commentsummary =bjson('productCommentSummary')
# 
# =============================================================================

    def stars_parse(self, response):
        print ("stars")
 
        item = response.meta['item']
     
        # response.body是一个json格式的
#        print
        js = json.loads(response.body)
#        print (js)
        # js = json.loads(str)
        # print js['CommentsCount'][0]['Score1Count']
        item['info'].append(js['CommentsCount'][0]['Score1Count'])
        item['info'].append(js['CommentsCount'][0]['Score2Count'])
        item['info'].append(js['CommentsCount'][0]['Score3Count'])
        item['info'].append(js['CommentsCount'][0]['Score4Count'])
        item['info'].append(js['CommentsCount'][0]['Score5Count'])
        item['info'].append(js['CommentsCount'][0]['CommentCount'])
        
        print (item)
        
        comment_total = int(item['info'][5])


       
        if comment_total % 10 == 0:  # 算出评论的页数，一页10条评论
            page = int(comment_total/10)
        else:
            page = int(comment_total/10 + 1)
        for k in range(0, min(page,100)):
#            url = "http://sclub.jd.com/productpage/p-""-s-0-t-3-p-" + str(k)\
#                  + ".html"
#                  
                  
            url = 'https://sclub.jd.com/comment/productPageComments.action?productId=' + item['productID'] + '&score=0&sortType=5&page='+ str(k)+'&pageSize=10&isShadowSku=0&rid=0&fold=1'
#            url = 'https://sclub.jd.com/comment/productPageComments.action?productId=' + item['productID'] + '&score=0&sortType=5&page='+ '7814515'+'&pageSize=10&isShadowSku=0&rid=0&fold=1'
            yield scrapy.Request(url, callback=self.comment_parse, meta={"item": item}) 
        yield item


        
        
    def comment_parse(self, response): 
        item = response.meta['item']
        str = response.body.decode("gbk").encode("utf-8")
        js = json.loads(str)
        comments = js['comments']  # 该页所有评论
        items = []
#        print ('zhltest2'+str)
        for comment in comments:
            item1 = JdCommentItem()
            if comment['id']=='':
                continue
            item1['user_name'] = comment['nickname']
            item1['user_ID'] = comment['id']
            item1['userProvince'] = comment['userProvince']
            item1['content'] = comment['content']
            item1['good_ID'] = comment['referenceId']
            item1['good_name'] = comment['referenceName']
            item1['date'] = comment['referenceTime']
            item1['replyCount'] = comment['replyCount']
            item1['score'] = comment['score']
            item1['status'] = comment['status']
            title = ""
            if 'title' in comment:
                item1['title'] = comment['title']
            item1['title'] = title
            item1['userRegisterTime'] = comment['nickname']
            item1['productColor'] = comment['productColor']
            item1['productSize'] = comment['productSize']
            item1['userLevelName'] = comment['userLevelName']
            item1['isMobile'] = comment['isMobile']
            item1['days'] = comment['days']
            tags = ""
            if 'commentTags' in comment:
                for i in comment['commentTags']:
                    tags = tags + i['name'] + " "
            item1['commentTags'] = tags
            items.append(item1)

        df= pd.DataFrame(items)  
        df.to_csv('comments/'+item['shopname']+'-'+item['productID'],mode='a')
       


#    def next_parse(self, response):
##        response.xpath('/div[@class="p-price"]/strong/i/text()').extract()
#    # 处理每条留言
#        for quote in response.xpath('//li[@class="gl-item"]/div'):
#            print('test2')
#            item = JdmaotaoItem()
#            item['price'] = quote.xpath('div/div[@class="p-price"]/strong/i/text()').extract_first()
#            item['name'] = quote.xpath('div/div[contains(@class,"p-name")]/a/@title').extract_first()
#            item['commit'] = quote.xpath('div/div[@class="p-commit"]/strong/a/text()').extract_first()
#            item['url'] = quote.xpath('div/div[@class="p-name p-name-type-2"]/a/@href').extract_first()
#            yield item
#
##        headers = {'referer': response.url}
#        # 后三十页的链接访问会检查referer，referer是就是本页的实际链接
#        # referer错误会跳转到：https://www.jd.com/?se=deny
#        if self.page < 100:
#            self.page += 1
#            yield scrapy.Request(self.url % (self.keyword, self.keyword, self.page), callback=self.parse)
#
#            
#        
#        # 翻到下一页，进行递归解析
#        next_page = response.css('li.next a::attr(href)').extract_first()
#        if next_page is not None:
#            # 这里是生成完整的链接
#            next_page = response.urljoin(next_page)
#            yield scrapy.Request(next_page, callback=self.parse)
#


