#coding=utf-8
__author__ = 'PC'
from flask import Flask, render_template,request,jsonify
import sae.const
import MySQLdb
try:
    from sae.storage import Bucket
except:
    pass
import json
isLocal=True
app = Flask(__name__)
app.debug = True
@app.route('/')
def index():
	return render_template('index1.html')

@app.route('/getdata', methods=['POST', 'GET'])
def getdata():
    if request.method == 'POST':
        values=request.values['dataId']
        jsonData={'dataId':values}
        db=MySQLdb.connect(host=sae.const.MYSQL_HOST,port=int(sae.const.MYSQL_PORT),user=sae.const.MYSQL_USER,passwd=sae.const.MYSQL_PASS,db=sae.const.MYSQL_DB,charset='utf8')
        # db.query("""SELECT * FROM mysql0571 WHERE AK编号='"""+values +"' or G编号='"+values+"' or D编号='"+values+"'")
        db.query("""SELECT * FROM mysql0571 WHERE AK编号='"""+'test1'+"'")
        r=db.store_result()
        myRow=r.fetch_row(r.num_rows())
        jsonData = {'data': [myRow]}
        return jsonify(jsonData)
    else:
        db=MySQLdb.connect(host=sae.const.MYSQL_HOST,port=int(sae.const.MYSQL_PORT),user=sae.const.MYSQL_USER,passwd=sae.const.MYSQL_PASS,db=sae.const.MYSQL_DB,charset='utf8')
        db.query("""SELECT * FROM mysql0571""")
        r=db.store_result()
        myRow=r.fetch_row(r.num_rows())
        jsonData = {'data': [myRow]}
        return jsonify(jsonData)

if __name__ == '__main__':
    app.run()
