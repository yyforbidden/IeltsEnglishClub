# -*- coding: utf-8 -*-
import messages
import httplib
import re
import HTMLParser
import logging
import os
from models import SinaBlogDatabase
        
class SinaBlogHandler:
    
    def __init__(self, **kargs):
        db = SinaBlogDatabase()
        cat = db.execute('select * from columns')
        db.close()
        self.category = dict((c[0], (c[1], c[2])) for c in cat)
        msg = '\n'.join('%s: %s' % (k, v[1]) for k, v in self.category.items())
        self._help_msg = 'Welcome to IELTS English Club!\n' + msg
        logging.debug(os.curdir)
        f = open('./ieltsenglishclub/welcome')
        self._welcome = f.read()
        f.close()
        self._host = 'blog.sina.com.cn'
        self._pic = 'http://p7.sinaimg.cn/2962006310/180/42641413018560'
        self._cat_url_tmplt = '/s/articlelist_2962006310_%d_1.html'
        self._pattern = re.compile(r'\<span class=\"atc_title"\>\s*\<a title=\"([^"]+)\"\s+.*href=\"([^"]+)\"\>.*\</span\>')

    def _parse_data(self, data):
        articles = []
        p = HTMLParser.HTMLParser()
        l = self._pattern.findall(data)
        for item in l:
            title = p.unescape(item[0].decode('utf-8'))
            url = item[1]
            a = dict(Title=title, Description=title, PicUrl=self._pic, Url=url)
            articles.append(a)
        return articles
    
    def _fetch_article_list(self, cat):
        cat_number = self.category[cat][0]
        conn = httplib.HTTPConnection(self._host)
        url = self._cat_url_tmplt % cat_number
        conn.request('GET', url)
        rsp = conn.getresponse()
        data = rsp.read()
        articles = self._parse_data(data)
        return articles
        
    def _send_welcome(self, msg):
        rsp = messages.WechatTextResponse(msg, Content=self._welcome)
        return rsp
    
    def _send_help(self, msg):
        rsp = messages.WechatTextResponse(msg, Content=self._help_msg)
        return rsp
    
    def _send_articles(self, msg, cat):
        db = SinaBlogDatabase()
        r = db.execute("select stat from columns where keyword='%s'" % cat)
        stat = r[0][0] + 1
        db.execute("update columns set stat=%d where keyword='%s'" % (stat, cat))
        db.close()
        articles = self._fetch_article_list(cat)
        article_count = len(articles)
        first = {'Title': 'IELTS English Club',
                'Description': u'IELTS English Club',
                'PicUrl': self._pic,
                'Url': 'http://blog.sina.com.cn/ieltsenglishclub'}
        last = {'Title': u'更多内容...',
                'Description': u'IELTS English Club',
                'PicUrl': self._pic,
                'Url': ('http://'+ self._host + self._cat_url_tmplt) %
                        self.category[cat][0]}
        if article_count > 4:
            articles = articles[:4]
            articles.append(last)
            article_count = 5
        articles = [first] + articles
        article_count += 1
        if article_count != 1:
            rsp = messages.WechatNewsResponse(msg, 
                                              ArticleCount=article_count,
                                              Articles=articles)
        else:
            rsp = None
        return rsp
    
    def on_event_subscribe(self, msg):
        return self._send_welcome(msg)
        
    def on_event_click(self, msg):
        cat = msg.EventKey
        return self._send_articles(msg, cat)
    
    def on_message_text(self, msg):
        data = msg.Content.lower()
        for k in self.category.keys():
            if data.startswith(k):
                return self._send_articles(msg, k)
        return None
            
    def on_keyword_help(self, msg):
        return self._send_help(msg)

