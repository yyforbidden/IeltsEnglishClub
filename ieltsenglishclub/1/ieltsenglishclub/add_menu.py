# -*- coding: utf-8 -*-
import messages as msg
import urllib, urllib2
import json
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

menu = {"button": 
        [{"name": "经验",
          "sub_button": [{"type": "click", "name": "考官提示", "key": "tips"},
                       {"type": "click", "name": "writing", "key": "writing"},
                       {"type": "click", "name": "speaking", "key": "speaking"},
                       {"type": "click", "name": "阅读听力", "key": "readlisten"},
                       {"type": "click", "name": "移民经验", "key": "emigration"},
                       ]},
         {"name": "群练习",
          "sub_button": [{"type": "click", "name": "练习组", "key": "practice"},
                       {"type": "click", "name": "写作题库", "key": "topic"},
                       {"type": "click", "name": "口语题库", "key": "speaking_topic"},
                       {"type": "click", "name": "词伙", "key": "words"},
#                        {"type": "click", "name": "最新真题", "key": "realtest"},
                       ]},
         {"name": "关于我们",
          "sub_button": [{"type": "click", "name": "介绍", "key": "intro"},
                       {"type": "click", "name": "合作考官", "key": "examiner"},
                       {"type": "click", "name": "常用工具", "key": "tools"},
                       {"type": "view", "name": "邀请好友", "url": "http://blog.sina.com.cn/s/blog_b08ca1260102vpeb.html"},
                       ]},
         ]}
    
wechat_host = 'api.wechat.qq.com'
# menu_str = urllib.urlencode(menu)
# print menu

at = msg.AccessToken('wxa7a1e9b980782576', 
                     '79cbf1dba727d8538c95cea1c95cc89b')
  
print at.access_token

url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % at.access_token
req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')
req.add_header('encoding', 'utf-8')
response = urllib2.urlopen(req, json.dumps(menu, ensure_ascii=False))
result = response.read()
print result
