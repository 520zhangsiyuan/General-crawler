#coding=utf-8
# from modle_test import XpathSpider
import requests
url = "http://192.168.1.133:8000"
#path = "C:/Users/ZSY/Desktop/Restful_API-master/API/wsgi.py"
#print (path)
#files = {'file': open(path, 'rb')}
r = requests.post(url, data={'url':'http://jx.tmall.com'})
print (r.text)
# a = '[img, a.brandItem, div.clearfix.J_brandBox, div.brand-content.clearfix, div.brand, div.container, div#content, div#mallPage.mui-global-biz-mallfp, body, html.ks-webkit537.ks-webkit.ks-chrome68.ks-chrome, document, Window]'
# c = {}
# c = XpathSpider(a).start_page()
# print (c)
