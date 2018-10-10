# -*-coding=utf-8-*-
import os
import re
import time
from urllib.parse import urljoin
from selenium import webdriver
# import requests
# from bs4 import BeautifulSoup
# import sys
# #from urllib import unquote
# #from url_decode import urldecode
class GovSpider:
    '''
        下载网页源码模块
    '''
    def __init__(self,url):
        print (url)
        self.site_url = url
        self.html3 = ''
        #本地新建文件根据site_url来命名，根据windows命名规则对其进行处理
        p1 = re.sub('\.', '', re.sub('.*//', '', self.site_url))
        p2 = re.sub('/', '', p1)
        p3 = re.sub(':', '', p2)
        p4 = re.sub('\?', '', p3)
        p5 = re.sub('"', '', p4)
        p6 = re.sub('<', '', p5)
        p7 = re.sub('>', '', p6)
        self.spath =re.sub('\*', '', p7)
        sindex = self.spath.find('/')
        if sindex != -1:
            self.spath = self.spath[:sindex]
        self.base_path = 'E:/' + self.spath
        print('base:', self.base_path)


    def start_page(self):
        #初始化webdriver，并给出chromedriver路径节省初始化时间
        req = webdriver.Chrome('E:/python/chromedriver.exe')
        #因ajax加载原因将模拟浏览器全屏
        req.maximize_window()

        #访问网址
        req.get(self.site_url)

        #webdriver隐式等待40秒
        req.implicitly_wait(40)
        #req.find_element_by_xpath("//div[@class='close']").click()
        #将页面向下翻，以便ajax加载
        for i in range (1,20):
            j = 500 * i
            js = "var q=document.documentElement.scrollTop="+str(j)
            req.execute_script(js)
            time.sleep(1)
        #因淘宝特殊性对其进行二次加载等待
        if 'taobao' in self.site_url:
            #js = "var q=document.documentElement.scrollTop=50"
            for i in range(1, 20):
                j = 500 * i
                js = "var q=document.documentElement.scrollTop=" + str(j)
                req.execute_script(js)
                time.sleep(1)

            #req.execute_script(js)
            #locator = (By.CLASS_NAME,'J_MemberAvatar member-avatar')
            #WebDriverWait(req, 20, 0.5,False).until(EC.presence_of_element_located(locator))
        #获取网页源码
        html1 = req.page_source
        #soup = BeautifulSoup(html1, 'html.parser')
        #iframes = soup.findAll('iframe')
        #将源码赋给新值，以便后期对其进行处理
        self.html3 = html1
        #html1 = re.sub('.*//')

        #print(html3)
        url = self.gs_runner(html1)

        '''
        if iframes:
            print('有隐藏页面:', iframes)
            for ifr_url in iframes:


                if 'https:' not in ifr_url or 'http' not in ifr_url:
                    ifr_url = urljoin(self.site_url, ifr_url.get('src'))
                    print('进入隐藏页面：', ifr_url, '，并开启隐藏页面抓取img、css、js的程序........')
                try:
                    html2 = requests.get(ifr_url).text

                    print (html2)
                    self.html4 = html2
                    self.gs_runner(html2)
                except Exception as e:
                    print('隐藏页面的地址格式不正确,无法访问：', ifr_url)
            '''
        # 程序运行完毕，自动关闭浏览器
        req.quit()
        return url
    def replace_html(self,html):
        '''
            对页面进行处理，主要是对超链接进行处理
        '''
        js_old = re.findall(r"<head><script.*?>[\s\S]*</script>\s<meta", html)
        if js_old != []:
            #self.html3 = self.html3.replace(js_old[0], '<head>\n<meta')
            pass
        self.html3 = self.html3.replace('"//','"https://')
        self.html3 = self.html3.replace('\'//', '\'https://')
        #self.html3 = self.html3.replace('close', '')

        self.html3 = self.html3.replace('gbk"', 'utf-8"')
        self.html3 = self.html3.replace('gbk\'', 'utf-8\'')
        print (urljoin(self.site_url,'/'))
        self.html3 = self.html3.replace('"/', '"'+urljoin(self.site_url,'/'))
        self.html3 = self.html3.replace('"./', '"' + urljoin(self.site_url, '/'))
        self.html3 = self.html3.replace('\'/', '\'' + urljoin(self.site_url, '/'))
        self.html3 = self.html3.replace('</head>', '<meta charset="utf-8"/></head>')
        #if 'taobao' in self.site_url:
        self.html3 = self.html3.replace('.js', '' + urljoin(self.site_url, '/'))
        return self.download_html(self.html3)
        #for i in range 1:

    def download_html(self, html):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>正在下载网页源码>>>>>>>>>>>>>>>>>>>>>>>>>')
        path = 'E:/python/%s' % (self.spath + '/htmls/')
        if not os.path.exists(path):
            os.makedirs(path)
        paths = 'E:/python/%s' % (self.spath + '/htmls/' + self.spath + '.html')
        #在本地写入html源码并向其添加禁止点击事件的js
        with open('E:/python/%s' % (self.spath + '/htmls/' + self.spath + '.html'), 'w', encoding='utf-8') as f:
            f.write(html+'''
	  	   <script src="http://code.jquery.com/jquery-2.1.1.min.js"></script>
	  <script>
	    document.onclick = function(e){
        console.log(e);
        console.log(e.path)
		 e.stopPropagation();
        e.preventDefault();
    	 let arr = [];
		if(e.target.cellIndex != ""){
				str ='*'+e.target.cellIndex;
				arr.push(str);
			}
        for(let i=0;i<e.path.length;i++){
            let className = e.path[i].className;
            if(className){
                className = className.split(" ");
            }
            let str = e.path[i].localName;
            if(e.path[i].id){
                str+="#"+e.path[i].id
            };
            if(className && className.length){
                for(let j=0;j<className.length;j++){
                    if(!className[j] || className == " ") continue;
                    str+="."+className[j]
                }
            }
            if(!str) continue;
            arr.push(str);

        }
        $.ajax({
        	url:"http://192.168.1.133:8000",
        	type:"post",
        	data:{
        		tags:arr.toString(),
        		urls:window.location.pathname
        	},
        	success:function(res){
        		console.log(res);
        	},
        	error:function(res){
        		console.log(res);
        	}
        });



        return false;
    }


</script>

''')

        return paths
    def gs_runner(self, html):
        return self.replace_html(html)

if __name__ == '__main__':
    gs = GovSpider()
    gs.start_page()