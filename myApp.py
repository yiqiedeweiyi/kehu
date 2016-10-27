#coding=utf-8
__author__ = 'PC'
from flask import Flask, render_template,request,jsonify
import sae.const
import _mysql
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
        print(request.values)
        jsonData=set()
        if isLocal:
            file=open('data.txt','r')
            jsonData=json.loads(file.readline())
        else:
            bucket = Bucket('filebucket')
            jsonData=json.loads(bucket.get_object_contents('data.txt'))
        return jsonify(jsonData)
    else:

        db=_mysql.connect(host=sae.const.MYSQL_HOST,port=int(sae.const.MYSQL_PORT),user=sae.const.MYSQL_USER,passwd=sae.const.MYSQL_PASS,db=sae.const.MYSQL_DB)
        db.query("""SELECT * FROM mysql0571""")
        r=db.store_result()
        myRow=r.fetch_rows()
        jsonData = {'data': [myRow[1]]}
        return jsonify(jsonData)

if __name__ == '__main__':
    app.run()
