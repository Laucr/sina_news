# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class FilePipeline(object):
    def process_item(self, item, spider):
        title = item['title']
        intro = item['article']
        category = item['category'].encode('gbk')
        file_root_dir = 'book_intro'
        category_dir = os.path.join(file_root_dir, category)
        if not os.path.exists(file_root_dir):
            os.mkdir(file_root_dir)
        if not os.path.exists(category_dir):
            os.mkdir(category_dir)
        if intro is not '':
            with open(category_dir + '/' + title.encode('gbk') + '.txt', 'w') as f:
                f.write(intro)
                f.close()
        return item
