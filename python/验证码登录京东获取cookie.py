from flask import render_template
from flask import make_response
from flask import Flask, session, redirect, url_for, escape, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time,requests,os,sys

app = Flask(__name__)

app.secret_key = 'fkdjsaonkqfdlkjfadskjfadskljdsfklj'

@app.route('/')

def index():

    if 'tel' in session:

        tel = session['tel']

        return '登录用户名是:' + tel + '<br>' + \
        "<b><a href = '/logout'>点击这里注销</a></b><b><a href = '/static/push.html'>点击这里获推送二维码</a></b>"
    return "您暂未登录， <br><a href = '/login'></b>" + \
         "点击这里登录</b></a>"
@app.route('/login', methods = ['GET', 'POST'])

def login():

    if request.method == 'POST':
        session['tel'] = request.form['tel']
        id = request.form['id']
        if id == "tel":
            a=request.form['tel']
            options=webdriver.ChromeOptions()
            # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
            options.add_argument('--headless')
    
            # 谷歌文档提到需要加上这个属性来规避bug
            options.add_argument('--disable-gpu')
    
            # 取消沙盒模式
            options.add_argument('--no-sandbox')
            options.add_argument('–incognito')
            options.add_argument('--disable-dev-shm-usage')
    
            # 指定浏览器分辨率
            options.add_argument('window-size=375x812')

            options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/92.0.4515.159"')
            driver =driver=webdriver.Chrome(options=options)
            driver.get('https://plogin.m.jd.com/login/login')
            driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/p[1]/input').clear()
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/p[1]/input').send_keys(a)
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/p[2]/button').click()
            blsz[a] = driver
            print(blsz)
            return "请提交验证码"
        else:
            yzm= request.form['yzm']
            a= request.form['tel']
            driver = blsz[a]
            print (driver)
            driver.find_element_by_xpath('//*[@id="authcode"]').clear()
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="authcode"]').send_keys(yzm)
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="app"]/div/p[2]/input').click()
            time.sleep(0.2)
            driver.find_element_by_xpath('//*[@id="app"]/div/a').click()
            time.sleep(0.2)
            #driver.get_screenshot_as_file("/tmp/test01.png")
            driver.get('https://m.jd.com')
            time.sleep(0.5)
            key = driver.get_cookie("pt_key")
            key = key["name"] + "=" + key["value"]+";"
            pin = driver.get_cookie("pt_pin")
            pin1 = pin["value"]
            pin = pin["name"] + "=" + pin["value"]+";"
            cookie = key + pin
            print(cookie)
            url = "http://127.0.0.1:8081/ql"#填写api接口地址
            payload = {"cookie": cookie,"pin":pin1}
            r = requests.post(url,data=payload)
            driver.close()
            return r.content
        return "error"
        
    return app.send_static_file('index1.html') #静态文件是别人搞的 

@app.route('/logout')

def logout():

   # remove the username from the session if it is there

   session.pop('tel', None)

   return redirect(url_for('index'))

@app.route('/restart')

def restart():
    os.system("ps aux|grep chrome |grep -v grep|cut -c 9-15|xargs kill -9")
    return "ok"
    

if __name__ == '__main__':
    blsz={}
    app.run("127.0.0.1", 8080)