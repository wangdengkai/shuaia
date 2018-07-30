'''
这个蜘蛛用来爬出, http://www.shuaia.net/  的图片
分析首页有个目录分类标签,
首页有一个目录按钮,点击后就会通过js自动加载出一个目录面板,
有多种分类,每个类别有地址
获取到地址后,分别请求,然后保存图片

'''

import scrapy
from selenium import webdriver

from shuaia.items import ShuaiaItem


class ShuaiaSpider(scrapy.Spider):
    #蜘蛛名称
    name = 'shuaia'

    def start_requests(self):
        #采用selenium获取列表
        #获取浏览器对象
        brower = webdriver.Chrome()
        #请求页面
        brower.get("http://www.shuaia.net/")
        #获取页面,点击目录按钮,
        brower.find_element_by_class_name("nav-link-icon").click()
        #获取所有a标签
        url_list=brower.find_elements_by_css_selector("#header ul li a")

        #遍历获取每一个网址和名称

        for url in url_list:
            name = url.text
            href = url.get_attribute("href")
            #发送请求
            yield scrapy.Request(url=href,callback=self.parse,meta={"category":name})

        #关闭浏览器
        brower.quit()

    def parse(self,response):
        '''
        用来处理每个分类的响应
        :param response:
        :return:
        '''
        #获取当前页面上所有的图片连接,请求图片进行处理
        #获取页面上所有的图片连接
        show_list= response.css('div[id^=post-] h2 a::attr(href)').extract()
        #便利,请求具体的每个页面
        # print(show_list)
        for detail_img in show_list:
            print("detail_img---%s" % detail_img)
            if detail_img is not None:
                yield scrapy.Request(detail_img,callback=self.content)
        #获取当前页面的下一页,有就请求,没有就不请求
        next_url = response.css('.pagination a[class="next"]::attr(href)').extract_first()
        if next_url is not None:
            #有下一页,请求
            yield scrapy.Request(next_url,callback=self.parse)
    def content(self,response):
        item = ShuaiaItem()
        item['name']=response.css("#container-single .wr-single-right .wr-sigle-intro h1::text").extract_first()
        print(item['name'])
        item['ImgUrl']=response.css(".wr-single-content-list p img::attr(src)").extract_first()
        item['ImgUrl']=response.urljoin(item['ImgUrl'])
        print("item---content----before")

        yield item
        # print("item---content----after")

        #获取下一个图片
        next_url = response.css('.pagination ul li a[class="next"]::attr(href)').extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url,callback=self.content)