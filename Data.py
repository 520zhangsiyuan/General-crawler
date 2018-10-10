# -*-coding=utf-8-*-

from lxml import html
def data_handle(xpaths,path):
    html_text = ''
    with open(path,'r',encoding='UTF-8') as f:
        html_text = f.read()
    img = ''
    text_list = []
    img_list = []
    a_list = []
    text = ''
    a = ''
    content = html.etree.HTML(html_text)
    print(xpaths)
    #if  xpaths['img'] != '':
       # xpaths['text'] = ''
    #for i in range (1,len(xpaths['a'])):
       # print(len(xpaths['a']))
    if xpaths['text'] != '':
        text = content.xpath(xpaths['text'] + '/text()')
        if xpaths['text'].endswith('td'):
            text = content.xpath(xpaths['text']+'[1]'+'/text()')
            #for i in range (1,10):
             #   text = content.xpath(xpaths['text'] +'['+str(i)+ ']/text()')
        if 'input' in xpaths['text']:
            text = content.xpath(xpaths['text'])
        for index in range(0,len(text)):

        #      #links[index]返回的是一个字典
            #print (text)
            result = text[index].strip()
            #print(result)
            if result != '':
               text_list.append(result)
        #print (text)
        # for i in text:
        #     text = i.xpath('string(.)').encode('utf-8').strip()
        #     text_list.append(text)
    if xpaths['a'] != '':
        a = content.xpath(xpaths['a'])
        # print(a[i])
        # a_list.append(a[i])

    if xpaths['img'] != '':
        img = content.xpath(xpaths['img'])
        # print(img[i])
        # img_list.append(img[i])
    collect = {'text':text_list,'a':a,'img':img}
    print (collect)
    return  collect
