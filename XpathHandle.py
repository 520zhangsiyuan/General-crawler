# -*-coding=utf-8-*-
import re
class XpathSpider:
    '''
        根据客户端提交标签进行处理并返回Xpath
    '''
    def __init__(self,tags):

        self.tags = tags.split(',')[0:7][::-1] #对标签数据进行处理
        print(self.tags)
        self.xpath = ''
        self.xpath_img = ''
        self.xpath_a = ''
    def start_page(self):
        '''
            处理方法如果有a和img标签就都返回并查看a标签是否有文本数据
        '''
        for tag in self.tags:
            tab1 = ''
            str_num = '1'
            #num = '5'
            if '.' in tag and '#' in tag:
                tab = tag.split('#')[0]
                print(tab)
                attribute = tag.split('.')[1]
                type = 'class'
            elif '.' in tag:
                tab = tag.split('.')[0]
                attribute = tag.split('.')[1]
                # if len(tag.split('.')) > 2:
                #     tab1 = ' '+tag.split('.')[2]
                type = 'class'
                print (tab+'  class '+attribute)
            elif 'undefined' in tag:
                print(tag)
                continue
            elif '*' in tag:
                type = 'num'
                tab = tag.split('*')[1]
                print (tab)
            elif '#' in tag :
                tab = tag.split('#')[0]
                attribute = tag.split('#')[1]
                # if len(tag.split('#')) > 2:
                #     tab1 = ' '+tag.split('.')[2]
                type = 'id'
                print (tab + ' id    ' +attribute)

            else:
                tab = tag
                type = ''
                attribute = ''
                print (tab)
            tab = tab.replace(' ', '')
            #print(num)
            if 'high' in attribute:
                attribute = ''
                type = ''
            if tab == 'a':
                xpath = '/'+tab+'/@href'
            elif tab == 'img':
                xpath = '/'+tab +'/@src'
            elif tab == 'span':
                xpath ='//'+tab
            elif tab == 'li':
                xpath = '//'+tab
            elif tab == 'strong':
                xpath = '//' + tab
            elif tab == 'input':
                xpath = '//' + tab + '[contains(@' + type + ',\'' + attribute + '\')]//@value'
            elif type == '':
                xpath = '//' + tab
            elif type == 'num':
                xpath = '[' + str(int(tab)+1)+']'
            else:
                xpath = '//'+tab+'[contains(@'+type+',\''+ attribute+'\')]'
            self.xpath = self.xpath + xpath
        #对生成xpth进行进一步处理并返回
        if 'a/@href' in self.xpath and 'img' in self.xpath:
            self.xpath_img = self.xpath.replace('/@href','')
            self.xpath_a = self.xpath.replace('/img/@src', '')
            self.xpath = self.xpath.replace('/@href', '').replace('/img/@src', '')
        elif 'a/@href' in self.xpath:
            self.xpath_a = self.xpath
            self.xpath = self.xpath.replace('/@href', '')
        elif 'img' in self.xpath:
            self.xpath_img = self.xpath
            #self.xpath = self.xpath.replace('/@src', '')
        self.xpath_a = re.sub('/@href.*', '/@href', self.xpath_a)
        self.xpath_img = re.sub('/@src.*', '/@src', self.xpath_img)
        xpaths = {'text':self.xpath,'a':self.xpath_a,'img':self.xpath_img}
        print (xpaths)
        return xpaths
if __name__ == '__main__':
    #pass
     xs = XpathSpider('a#J_Itemlist_TLink_568760604838.J_ClickStat,div.row.row-2.title.xh-highlight,div.ctx-box.J_MouseEneterLeave.J_IconMoreNew,div.item.J_MouserOnverReq,div.items,div.grid.g-clearfix,div.m-itemlist,div#minisrp-itemlist,div.grid-total,div#main.srp-main,div#page.srp-page,body.response-wider,html.ks-webkit537.ks-webkit.ks-chrome68.ks-chrome')
     xs.start_page()