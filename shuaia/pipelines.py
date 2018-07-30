# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


# class ShuaiaPipeline(object):
#     def process_item(self, item, spider):
#         return item

class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self,item,info):
        print("------------------")
        yield Request(item['ImgUrl'],meta={'item':item['name'],
                                           'image':item['ImgUrl']})


    def file_path(self,request,response=None,info=None):
        name = request.meta['item']
        #清除window乱包的字符
        name =re.sub(r'[？\\*|“<>:/()0123456789]', '', name)
        image_guid = request.url.split('/')[5]

        img_url = request.meta['image']
        img_name=img_url.split('/')[-1]
        filename = 'full/{0}/{1}'.format(image_guid,name+".jpg")
        return filename


    def item_completed(self, results, item, info):
        image_path=[x['path'] for ok ,x in results if ok]

        if not image_path:
            raise DropItem("不存在这个图片")

        item['image_paths'] = image_path
        return item