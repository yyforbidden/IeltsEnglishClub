from messages import WechatError

class Dispatcher:
    
    _message_types = ['text', 'image', 'voice',
                      'video', 'shortvideo',
                      'location', 'link']
    
    _msg_handler_prefix = 'on_message_'
    _evt_handler_prefix = 'on_event_'
    _kwd_handler_prefix = 'on_keyword_'
    
    _keyword_handlers = {}
    _event_handlers = {}
    _message_handlers = {}
    
    @staticmethod
    def _void_handler(msg):
        return ''
    
    @classmethod
    def message_handler(self, msg):
        handler = None
        if msg.MsgType == 'text':
            c = msg.Content.lower()
            for k in self._keyword_handlers:
                if c.startswith(k):
                    handler = self._keyword_handlers[k]
        if not handler:
            handler = self._message_handlers.get(msg.MsgType,
                                                 self._void_handler)
        return handler
    
    @classmethod
    def event_handler(self, msg):
        evt = msg.Event.lower()
        return self._event_handlers.get(evt, self._void_handler)
    
    @classmethod
    def install_handler(self, handler_cls, **kargs):
        self.handler_obj = handler_cls(**kargs)
        
        for attr_name in dir(self.handler_obj):
            attr = getattr(self.handler_obj, attr_name)
            if not callable(attr):
                continue
            
            if attr_name.startswith(self._msg_handler_prefix):
                msg_type = attr_name.split(self._msg_handler_prefix)[-1]
                if msg_type not in self._message_types:
                    raise WechatError('Message type unknown during installing handler.')
                self._message_handlers[msg_type] = attr
            elif attr_name.startswith(self._kwd_handler_prefix):
                keyword = attr_name.split(self._kwd_handler_prefix)[-1]
                if keyword:
                    self._keyword_handlers[keyword.lower()] = attr
            elif attr_name.startswith(self._evt_handler_prefix):
                event = attr_name.split(self._evt_handler_prefix)[-1]
                if event:
                    self._event_handlers[event.lower()] = attr
            else:
                continue
            