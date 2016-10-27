#coding=utf-8
__author__ = 'PC'
from flask import Flask, render_template,request,jsonify
import sae.const
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

@app.route('/getdata', methods=['POST'])
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
        jsonData = {'data': [sae.const.MYSQL_DB,sae.const.MYSQL_USER ,sae.const.MYSQL_PASS,sae.const.MYSQL_HOST,sae.const.MYSQL_PORT,
                             sae.const.MYSQL_HOST_S]}
        return jsonify(jsonData)

@app.route('/setdata', methods=['POST', 'GET'])
def setdata():
    if request.method == 'POST':
        values=request.values['data']
        print(values)
        print(json.loads(values))
        jsonList=json.loads(values)['data']
        myJsonList=[]
        for i in range(len(jsonList)):
            orderNo=jsonList[i]['orderNo']
            title=jsonList[i]['title']
            contactName=jsonList[i]['contactName']
            fromDate=jsonList[i]['fromDate']
            toDate=jsonList[i]['toDate']
            roomName=jsonList[i]['roomName']
            roomNum=jsonList[i]['roomNum']
            isVisit=jsonList[i]['isVisit']
            isProcess=jsonList[i]['isProcess']
            myJsonList.append({'orderNo':orderNo,'title':title,'contactName':contactName,'fromDate':fromDate,'toDate':toDate,
                               'roomName':roomName,'roomNum':roomNum,'isVisit':isVisit,'isProcess':isProcess})
        jsonData={'data':myJsonList}
        if isLocal:
            file=open('data.txt','w')
            file.write(json.dumps(jsonData))
            file.close()
        else:
            bucket = Bucket('filebucket')
            bucket.put_object('data.txt',str(json.dumps(jsonData)))
            pass
        return jsonify(jsonData)
    else:
        jsonData = {'data': []}
        return jsonify(jsonData)

@app.route('/updateData', methods=['POST', 'GET'])
def updateData():
    if request.method == 'POST':
        response={'response':'修改数据不成功！'}
        orderId=request.values['orderId']
        isVisit=request.values['isVisit']
        orderId=orderId[8:]
        print(orderId)
        jsonData=set()
        if isLocal:
            file=open('data.txt','r')
            jsonData=json.loads(file.readline())
            file.close()
        else:
            bucket = Bucket('filebucket')
            jsonData=json.loads(bucket.get_object_contents('data.txt'))
        for i in range(len(jsonData['data'])):
            if(int(orderId)==jsonData['data'][i]['orderNo']):
                jsonData['data'][i]['isVisit']=isVisit
                jsonData['data'][i]['isProcess']='1'
                response={'response':'修改数据成功！'}
        if isLocal:
            file=open('data.txt','w')
            file.write(json.dumps(jsonData))
            file.close()
        else:
            bucket = Bucket('filebucket')
            bucket.put_object('data.txt',str(json.dumps(jsonData)))
        return jsonify(response)
    else:
        jsonData = {'data': []}
        return jsonify(jsonData)
if __name__ == '__main__':
    app.run()
