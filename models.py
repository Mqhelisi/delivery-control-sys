import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
db = SQLAlchemy()
'''
setup_db(app):
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
# "postgresql+psycopg2://postgres:Bukhosi04@localhost/delivery"
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:Mqhe23@localhost/zpckb"

    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    return db



class Unit(db.Model):
    __tablename__ = 'unit'
    
    unit_id = db.Column(db.Integer, nullable=False, primary_key=True)
    capacityMW = db.Column(db.Integer, nullable=False)
    lastAM = db.Column(db.Date, nullable=False)
    
    def __init__(self, unit_id,capacityMW,lastAM):
        self.unit_id = unit_id
        self.capacityMW = capacityMW
        self.lastAM = lastAM
        
    def json(self):
        return {
            'unit_id':self.unit_id,
            'capacityMW': self.capacityMW,
            'lastAM': self.lastAM
        }
    
    
class GGB(db.Model):
    __tablename__ = 'gen_guide_bearing'
    
    id= db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, unit,value,date):
        self.unit = unit
        self.value = value
        self.date = date
        
    def json(self):
        return {
            'unit':self.unit,
            'value': self.value,
            'date': self.date
        }
    
class GTB(db.Model):
    __tablename__ = 'thrust_bearing'
    
    id= db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, unit,value,date):
        self.unit = unit
        self.value = value
        self.date = date
        
    def json(self):
        return {
            'unit':self.unit,
            'value': self.value,
            'date': self.date
        }
    
class TGB(db.Model):
    __tablename__ = 'turb_guide_bearing'
    
    id= db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Numeric, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, unit,value,date):
        self.unit = unit
        self.value = value
        self.date = date
        
    def json(self):
        return {
            'unit':self.unit,
            'value': self.value,
            'date': self.date
        }