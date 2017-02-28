# _*_ coding: utf-8 _*_

from robotapp import app
from robotapp import db
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy

class LightValue(db.Model):
    __tablename__ = 'light_value'
    id = db.Column(db.Integer, primary_key = True)
    mac = db.Column(db.String(8))
    time = db.Column(db.Integer)
    light = db.Column(db.Float)
    
    def __init__(self, mac, time, light):
        self.mac = mac
        self.time = time
        self.light = light
    
    def __repr__(self):
        return '<Mac %r Time %d, Light %f>' % (self.mac, self.time, self.light)


