from flask import request, abort, make_response, render_template
from ieltsenglishclub import app
import logging
import messages
from dispatcher import Dispatcher
from models import SinaBlogDatabase

@app.route("/wechat", methods=["GET"])
def wechat_verify():
    data = request.args
    if not data:
        logging.error('No data in authentication request')
        abort(401)
        
    signature = data.get("signature", None)
    nonce = data.get("nonce", None)
    timestamp = data.get("timestamp", None)
    
    if None in [signature, nonce, timestamp]:
        logging.error('Mandatory data missed in authentication request')
        abort(401)
        
    if not messages.verify_token(signature,
                                 app.config['APP_TOKEN'],
                                timestamp,
                                nonce):
        logging.error('Verify failed in authentication')
        abort(401)
    else:
        echostr = data.get("echostr", None)
        return make_response(echostr)
                

@app.route('/wechat', methods=['POST'])
def message_received():
    data = request.stream.read()
    msg = messages.WechatRequest(data)
    logging.debug('Received: ' + data)
    
    if msg.MsgType != 'event':
        handler = Dispatcher.message_handler(msg)
    else:
        handler = Dispatcher.event_handler(msg)
    if handler:
        result = handler(msg)
        if result:
            rsp = unicode(result)
            logging.debug('Sent: ' + rsp)
            return make_response(rsp)
    return ''

@app.route('/stat')
def stat():
    db = SinaBlogDatabase()
    stat = db.execute("select description, stat from columns")
    return render_template('stat.html', stat=stat)

