from flask import Flask
import os
from app import db
import pandas
import stringCutting
from datetime import datetime
from config import Config
from app.models import Date, StockShares, Company

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object(Config)
sharesDir = '/sharesBase/'



dateList  = stringCutting.extractDate()
for date in dateList:
    somedayStock = datetime.strptime(date,'%Y-%m-%d').date()

    output_filename = somedayStock.strftime('listaAkcji-%Y-%m-%d.csv')
    db.create_all()

    #Checking if given day is already in our DB
    exists = db.session.query(Date.day).filter_by(day=somedayStock).scalar() is not None
    if exists :
        print('Day ' + date + ' already exists in database ')
        continue
    print('Adding day: ' + date)
    sd = Date( day = somedayStock )
    db.session.add(sd)
    db.session.commit()

    df = pandas.read_csv(basedir + sharesDir + output_filename, na_values='—'
                         , dtype={'Kurs(PLN)': float, 'Zmiana(%)': float, 'Otwarcie': float, 'Min': float, 'Max': float,
                                  'Obrot(szt)': float, 'Obrot(PLN)': float})
    df = df.fillna(0) # all NA/NAN records are filled with '0'

    rows = []
    rows = df.to_records(index=False)
    for row in rows:
        notExists = db.session.query(Company.name).filter_by(name=row[0]).scalar() is None
        if notExists:
            sn = Company(name=row[0])
            db.session.add(sn)
            db.session.commit()
            print('Adding Company:' + row[0])

        ss = StockShares(price = row[1], change = row[2], opening = row[3], min_v = row[4], max_v = row[5], trading_pcs = row[6], trading_px = row[7], date = somedayStock, stockName = row[0])
        db.session.add(ss)
        db.session.commit()


