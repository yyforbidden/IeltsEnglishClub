import messages

class DemoHandler:
    
    def __init__(self, **kargs):
        pass
    
    def on_message_text(self, msg):
        text = 'I received text message ' + msg.Content
        rsp = messages.WechatTextResponse(msg, Content=text)
        return rsp
    
    def on_message_image(self, msg):
        picurl = msg.PicUrl
        mediaid = msg.MediaId
        text = 'I received image message: %s, %s' %(picurl, mediaid)
        rsp = messages.WechatTextResponse(msg, Content=text)
        return rsp

    def on_message_voice(self, msg):
        fmt = msg.Format
        mediaid = msg.MediaId
        text = 'I received voice message: %s, %s' %(fmt, mediaid)
        rsp = messages.WechatTextResponse(msg, Content=text)
        return rsp
        
    def on_message_video(self, msg):
        thumbmediaid = msg.ThumbMediaId
        mediaid = msg.MediaId
        text = 'I received video message: %s, %s' %(thumbmediaid, mediaid)
        rsp = messages.WechatTextResponse(msg, Content=text)
        return rsp
    
    def on_message_shortvideo(self, msg):
        thumbmediaid = msg.ThumbMediaId
        mediaid = msg.MediaId
        text = 'I received shortvideo message: %s, %s' %(thumbmediaid, mediaid)
        rsp = messages.WechatTextResponse(msg, Content=text)
        return rsp

    def on_message_location(self, msg):
        x = msg.Location_X
        y = msg.Location_Y
        scale = msg.Scale
        label = msg.Label
        text = 'I received location message: %s, %s, %s, %s' % (x, y, scale, label)
        rsp = messages.WechatTextResponse(msg, Content=text)
        return rsp
        
    def on_message_link(self, msg):
        title = msg.Title
        desc = msg.Description
        url = msg.Url
        text = 'I received link message: %s, %s, %s' % (title, desc, url)
        rsp = messages.WechatTextResponse(msg, Content=text)
        return rsp

    def on_keyword_reverse(self, msg):
        text = msg.Content.split('>>>', 1)[1]
        text = ''.join(text[i] for i in range(len(text)-1, -1, -1))
        text = 'I received keyword "reverse", handled message: ' + text
        rsp = messages.WechatTextResponse(msg, Content=text)
        return rsp
        
    def on_keyword_upper(self, msg):
        text = msg.Content.split('>>>', 1)[1].upper()
        text = 'I received keyword "upper", handled message: ' + text
        rsp = messages.WechatTextResponse(msg, Content=text)
        return rsp
        
    def on_keyword_image(self, msg):
        rsp = messages.WechatImageResponse(msg, MediaId='aP-CjEx1Tctzcfm0pxn-bdHop3SJ92boIBB69UxXg164btoZa0OfvahGfI9hbxVo')
        return rsp
    
    def on_keyword_voice(self, msg):
        rsp = messages.WechatVoiceResopnse(msg, MediaId='e2vf2mubR_gBhvQ40JLk0LnIT1xH_m2kehepO0UzslTMO6MlshbsO2dLNk2kxEYe')
        return rsp

    def on_keyword_video(self, msg):
        rsp = messages.WechatVideoResponse(msg,
                                           MediaId='ACrGieaL1IbghT7NPuU8Eo7s_L5EMADJNpekAEVEXv4QurdzltGJMiNDcv7kAckm',
                                           Title='test video',
                                           Description='test video desc')
        return rsp
    
    def on_keyword_music(self, msg):
        rsp = messages.WechatMusicResponse(msg,
                                           Title='Test music',
                                           MusicUrl='http://emo.luoo.net/low/luoo/radio719/01.mp3',
                                           HQMusicUrl='http://emo.luoo.net/low/luoo/radio719/01.mp3',
                                           ThumbMediaId='')
        return rsp
    
    def on_keyword_news(self, msg):
        news = [{'Title': 'news1',
                 'Description': 'this is news1',
                 'PicUrl': 'http://pic3.zhimg.com/9411ed3419418f47a1213ff1ca52e2d6_b.jpg',
                 'Url': 'http://www.zhihu.com/question/22084816/answer/46896430'},
                {'Title': 'news2',
                 'Description': 'this is news2',
                 'PicUrl': 'http://pic3.zhimg.com/9411ed3419418f47a1213ff1ca52e2d6_b.jpg',
                 'Url': 'http://www.zhihu.com/question/22084816/answer/46896430'},]
        rsp = messages.WechatNewsResponse(msg, ArticleCount=len(news), Articles=news)
        return rsp
    
    def on_event_subscribe(self, msg):
        text = 'I received event "subscribe", welcome!'
        rsp = messages.WechatTextResponse(msg, Content=text)
        return rsp
    
