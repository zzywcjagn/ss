import requests,json
from flask import Flask,request

app = Flask(__name__)

#获取token
def gettoken():
    payload = {'client_id': client_id, 'client_secret': client_secret}
    r = requests.get(apiurl+"/auth/token", params=payload) 
    b=r.json()
    print(b['data']['token'])
    return b['data']['token']


#变量部分
client_id= "" #这里填写申请到的client_id
client_secret= ""#这里填写申请到的client_secret
qlurl= ""#填写青龙的地址根目录
apiurl=qlurl +"/open"
url= apiurl+"/envs?t=1633076856051"
token = gettoken()
headers={
    'Authorization':'Bearer '+token,
    'Origin':qlurl,
    'content-type':'application/json;charset=UTF-8'
}
pin=""


#搜索变量
def search(searchValue):
    payload1 = {'searchValue': searchValue}
    bb=requests.get (url=url,params=payload1,headers=headers)
    ssjg=bb.json()
    print (bb.json()['data'])
    if ssjg['data'] == []:
        return "error"
    else:
        ssjg=ssjg['data'][0]
        ssjg_cookie=ssjg['value']
        ssjg_id=ssjg['_id']
        ssjg_remarks=ssjg['remarks']
        return ssjg

#添加变量
def addenv(jdcookie,jdremarks):
    payload2 = [{
        'name': 'JD_COOKIE',
        'remarks':jdremarks,
        'value':jdcookie
        }]
    r = requests.post(url=url, data=json.dumps(payload2),headers=headers)
    return r.content

#更新变量
def updateenv(ssjg_remarks,jdcookie,ssjg_id):
    payload3 = {
        'name': "JD_COOKIE",
        'remarks': ssjg_remarks,
        'value': jdcookie,
        '_id': ssjg_id
        }
    gxbl=requests.put(url=url, data=json.dumps(payload3),headers=headers)
    return gxbl.content

@app.route('/ql', methods = ['POST'])
def index():
    pin= request.form['pin']
    if pin is not None:
        pin1= "pt_pin="+pin
        jdcookie=request.form['cookie']
        ssjg=search(pin1)
        if ssjg == "error":
            jg=addenv(jdcookie,pin)
        elif ssjg['value'] is not None:
            ssjg_id=ssjg['_id']
            ssjg_remarks=ssjg['remarks']
            jg=updateenv(ssjg_remarks,jdcookie,ssjg_id)
        else:
            return "error"
        return jg
    else:
        return "提交的参数错误"


if __name__ == '__main__':
    app.run("127.0.0.1", 8081)