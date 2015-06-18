import xml.etree.ElementTree as ET
from hashlib import sha1
import time
import json
import urllib
import httplib

def verify_token(signature, token, timestamp, nonce):    
    l = [token, timestamp, nonce]
    l.sort()
    s = sha1("".join(l)).hexdigest()
    
    if s == signature:
        return True
    else:
        return False
        
                 
class WechatError(Exception):
    pass


class WechatRequest:
    
    def __init__(self, data):
        self._data = data
        self._tree = ET.fromstring(self._data)
        self._fields = {}
        
    def __getattr__(self, attr):
        if attr in self._fields:
            return self._fields[attr]
        else:
            try:
                value = self._tree.find(attr).text
            except AttributeError:
                raise WechatError('Mandatory field missing in Wechat message!')
            self._fields[attr] = value
            return value
            
    def __repr__(self):
        return self._data
        
class WechatResponse:

    def __init__(self, req, msg_type, **kargs):
        self._from = req.FromUserName
        self._to = req.ToUserName
        self._time = str(int(time.time()))
        self._msg_type = msg_type
        self._build(**kargs)
        
    def __repr__(self):
        return self._data
    
    def _build(self, **kargs):
        _msg_tmplt = unicode("<xml>"+
                       "<ToUserName><![CDATA[%s]]></ToUserName>"+
                       "<FromUserName><![CDATA[%s]]></FromUserName>"+
                       "<CreateTime>%s</CreateTime>"+
                       "<MsgType><![CDATA[%s]]></MsgType>"+
                       "%s"+
                       "</xml>")
        paras = self._build_paras(**kargs)
        body = (self._from, self._to, self._time, self._msg_type, paras)
        self._data = _msg_tmplt % body
        
    def _build_paras(self, **kargs):
        # Dummy filler
        return ''
    

class WechatTextResponse(WechatResponse):
    
    def __init__(self, req, **args):
        WechatResponse.__init__(self, req, 'text', **args)

    def _build_paras(self, **kargs):
        para_tmplt = u"<Content><![CDATA[%s]]></Content>"
        paras = para_tmplt % kargs['Content']
        return paras


class WechatImageResponse(WechatResponse):
    
    def __init__(self, req, **args):
        WechatResponse.__init__(self, req, 'image', **args)

    def _build_paras(self, **kargs):
        para_tmplt = u'<Image><MediaId><![CDATA[%s]]></MediaId></Image>'
        paras = para_tmplt % kargs['MediaId']
        return paras
    
    
class WechatVoiceResopnse(WechatResponse):

    def __init__(self, req, **args):
        WechatResponse.__init__(self, req, 'voice', **args)

    def _build_paras(self, **kargs):
        para_tmplt = u'<Voice><MediaId><![CDATA[%s]]></MediaId></Voice>'
        paras = para_tmplt % kargs['MediaId']
        return paras
    
    
class WechatVideoResponse(WechatResponse):
    
    def __init__(self, req, **args):
        WechatResponse.__init__(self, req, 'video', **args)

    def _build_paras(self, **kargs):
        para_tmplt = u'<Video><MediaId><![CDATA[%s]]></MediaId>%s</Video>'
        title_tmplt = u'<Title><![CDATA[%s]]></Title>'
        desc_tmplt = u'<Description><![CDATA[%s]]></Description>'
        
        media_id = kargs['MediaId']
        title = kargs.pop('Title', None)
        desc = kargs.pop('Description', None)

        opt_para = ''
        if title is not None:
            opt_para += title_tmplt % title
        if desc is not None:
            opt_para += desc_tmplt % desc
        paras = para_tmplt % (media_id, opt_para)
        return paras
        
        
class WechatMusicResponse(WechatResponse):
    
    def __init__(self, req, **args):
        WechatResponse.__init__(self, req, 'music', **args)

    def _build_paras(self, **kargs):
        para_tmplt = u'<Music>%s<ThumbMediaId><![CDATA[%s]]></ThumbMediaId></Music>'
        title_tmplt = u'<Title><![CDATA[%s]]></Title>'
        desc_tmplt = u'<Description><![CDATA[%s]]></Description>'
        url_tmplt = u'<MusicUrl><![CDATA[%s]]></MusicUrl>'
        hq_url_tmplt = u'<HQMusicUrl><![CDATA[%s]]></HQMusicUrl>'
        
        title = kargs.pop('Title', None)
        desc = kargs.pop('Description', None)
        music_url = kargs.pop('MusicUrl', None)
        hq_music_url = kargs.pop('HQMusicUrl', None)
        thumb_media_id = kargs['ThumbMediaId']
        
        opt_para = ''
        if title is not None:
            opt_para += title_tmplt % title
        if desc is not None:
            opt_para += desc_tmplt % desc
        if music_url is not None:
            opt_para += url_tmplt % music_url
        if hq_music_url is not None:
            opt_para += hq_url_tmplt % hq_music_url
        paras = para_tmplt % (opt_para, thumb_media_id)
        return paras
    

class WechatNewsResponse(WechatResponse):
    
    def __init__(self, req, **args):
        WechatResponse.__init__(self, req, 'news', **args)

    def _build_paras(self, **kargs):
        para_tmplt = u'<ArticleCount>%s</ArticleCount><Articles>%s</Articles>'
        article_tmplt = u'<item>%s</item>'
        title_tmplt = u'<Title><![CDATA[%s]]></Title>'
        desc_tmplt = u'<Description><![CDATA[%s]]></Description>'
        pic_url_tmplt = u'<PicUrl><![CDATA[%s]]></PicUrl>'
        url_tmplt = u'<Url><![CDATA[%s]]></Url>'
        
        article_cnt = kargs['ArticleCount']
        articles = kargs['Articles']
        
        article_str = ''
        for a in articles:
            article = ''
            
            title = a.pop('Title', None)
            if title is not None:
                article += title_tmplt % title
            
            desc = a.pop('Description', None)
            if desc is not None:
                article += desc_tmplt % desc
            
            pic_url = a.pop('PicUrl', None)
            if pic_url is not None:
                article += pic_url_tmplt % pic_url
            
            url = a.pop('Url', None)
            if url is not None:
                article += url_tmplt % url
                
            article_str += article_tmplt % article
        
        paras = para_tmplt % (article_cnt, article_str)
        return paras


class AccessToken:
    
    def __init__(self, appid, secret):
        self._appid = appid
        self._secret = secret
        self._get_token()
        
    def __getattr__(self, attr):
        if attr == 'access_token':
            if time.time() - self._timestamp > self._threshold:
                self._get_token()
            return self._token
        else:
            raise AttributeError('Unknown attribute: %s' % attr)
        
    def _get_token(self):
        cmd = WechatGetAccessTokenCmd(grant_type='client_credential',
                                      appid=self._appid,
                                      secret=self._secret)
        result = cmd.send()
        if 'errcode' in result.keys():
            raise WechatError('Get token error: %s, %s' % 
                              (result['errcode'], result['errmsg']))
        self._token = result['access_token']
        self._threshold = result['expires_in'] - 120
        self._timestamp = time.time()
    

class WechatCmd:
    
    host = 'api.weixin.qq.com'
    
    def __init__(self, **kargs):
        self.body = kargs.pop('body', {})
        self.args = kargs
    
    def send(self):
        conn = httplib.HTTPSConnection(self.host)
        args_str = urllib.urlencode(self.args)
        url = self.url + '?' + args_str
        body = json.dumps(self.body)
        conn.request(self.method, url, body)
        rsp = conn.getresponse()
        return json.loads(rsp.read())
    
    
class WechatGetAccessTokenCmd(WechatCmd):
    url = '/cgi-bin/token'
    method = 'GET'


class WechatGetServerIpCmd(WechatCmd):
    url = '/cgi-bin/getcallbackip'
    method = 'GET'
    
    
class WechatAddKfAccountCmd(WechatCmd):
    url = '/customservice/kfaccount/add'
    method = 'POST'


class WechatModKfAccountCmd(WechatCmd):
    url = '/customservice/kfaccount/update'
    method = 'POST'
    
    
class WechatDelKfAccountCmd(WechatCmd):
    url = '/customservice/kfaccount/del'
    method = 'GET'


class WechatGetAllKfAccountCmd(WechatCmd):
    url = '/cgi-bin/customservice/getkflist'
    method = 'GET'


class WechatSendKfMessageCmd(WechatCmd):
    url = '/cgi-bin/message/custom/send'
    method = 'POST'


class WechatAddNewsCmd(WechatCmd):
    url = '/cgi-bin/material/add_news'
    method = 'POST'


class WechatGetMaterialCmd(WechatCmd):
    url = '/cgi-bin/material/get_material'
    method = 'GET'


class WechatDelMaterialCmd(WechatCmd):
    url = '/cgi-bin/material/del_material'
    method = 'GET'


class WechatUpdateMaterialCmd(WechatCmd):
    url = '/cgi-bin/material/update_news'
    method = 'POST'


class WechatGetMaterialCountCmd(WechatCmd):
    url = '/cgi-bin/material/get_materialcount'
    method = 'POST'
    
    
class WechatBatchGetMaterialCmd(WechatCmd):
    url = '/cgi-bin/material/batchget_material'
    method = 'POST'
    
class WechatAddMenuCmd(WechatCmd):
    url = '/cgi-bin/menu/create'
    method = 'POST'
    
class WechatGetMenuCmd(WechatCmd):
    url = '/cgi-bin/menu/get'
    method = 'GET'
    
class WechatDelMenuCmd(WechatCmd):
    url = '/cgi-bin/menu/delete'
    method = 'GET'
