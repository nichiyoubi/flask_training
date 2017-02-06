# _*_ coding: utf-8 _*_
from flask import Flask
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:Masanori1972@localhost/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 秘密鍵は後ほどランダム化する
app.config['SECRET_KEY'] = 'The secret key which ciphers the cookie'

import robotapp.views
