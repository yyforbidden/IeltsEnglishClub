from flask import Flask
import logging
from dispatcher import Dispatcher
from sina_blog_handler import SinaBlogHandler

logging.basicConfig(level=logging.DEBUG)

Dispatcher.install_handler(SinaBlogHandler)
app = Flask(__name__)
app.config.from_object('config')

import views