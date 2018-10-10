#!/usr/bin/env python
#--coding:utf-8--

from http.server import BaseHTTPRequestHandler, HTTPServer
from Download_page import GovSpider
from XpathHandle import XpathSpider
from socketserver import ThreadingMixIn
from Data import data_handle
from urllib.parse import urlparse
import shutil
from Ip_get import get_host_ip
import cgi
import io
import re


class user_HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
         sendReply = False
         querypath = urlparse(self.path)
         print(querypath)
         filepath, query = querypath.path, querypath.query
         print(filepath+'   '+query)
         try:
             with open ('E:'+filepath,'rb') as f:
                     content = f.read()
                     self.send_response(200)
                     self.send_header('Content-type','1')
                     self.end_headers()
                     self.wfile.write(content)
         except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     }
        )
        #self.wfile.write('Client: %s ' % self.client_address)
        #self.wfile.write('User-agent: %sn' % str(self.headers['user-agent']))
        #self.wfile.write('Path: %sn' % self.path)
        #self.wfile.write('Form data:n')
        self.tag = ''
        self.paths = ''
        for field in form.keys():
            field_item = form[field]
            #filename = field_item.filename
            filevalue = field_item.value
            #filesize = len(filevalue)  # 文件大小(字节)
            # print len(filevalue)
            #print (field)
            #print (filevalue)
            if field == 'url':
                if 'http:' not in filevalue and 'https:' not in filevalue:
                    filevalue = 'https://'+ filevalue
                print (filevalue)
                gs = GovSpider(filevalue)
                self.url1 = gs.start_page()
                self.url1 = re.sub('E:','',self.url1)
                print (self.url1)
                ip = get_host_ip()
                self.do_action(ip ,self.url1)
            elif field == 'urls':
                self.paths ='E:/'+filevalue[1:]
            elif field == 'tags':
                self.tag = filevalue
                #print (tag)
            if self.paths != ''and self.tag != '':
                xs = XpathSpider(self.tag).start_page()
                item = data_handle(xs,self.paths)
                self.do_data(item)
    def do_action(self,ip, args):
        self.outputtxt(ip+':8000'+args)

    def do_data(self, item):
        self.outputdata(item)
    def outputtxt(self, content):
        # 指定返回编码
        enc = "UTF-8"
        content = content.encode(enc)
        f = io.BytesIO()
        f.write(content)
        #f.write(str(self.client_address))
        f.seek(0)
        self.send_response(200)
        #解决跨域问题
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)

    def outputdata(self, item):
        # 指定返回编码
        enc = "UTF-8"
        #print (item)
        #item['text'] = str(item['text'])+']'
        #items = re.sub('<Element a at .{13}>.', '', str(item))
        items = str(item)
        content = items.encode(enc)
        f = io.BytesIO()
        f.write(content)
        # f.write(str(self.client_address))
        f.seek(0)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)
class ThreadingHttpServer( ThreadingMixIn, HTTPServer ):
    pass
def run():
    port = ''
    print('starting server, port', port)

    # Server settings
    server_address = ('192.168.1.133', port)
    #多线程访问
    httpd = ThreadingHttpServer(server_address, user_HTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()
    httpd.server_close()

if __name__ == '__main__':
    run()