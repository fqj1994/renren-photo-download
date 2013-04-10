#!/usr/bin/env python
# coding: utf-8

import mechanize
import re
import requests
import Image
from StringIO import StringIO

def get_album_list(sid, frienduid):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.12) Gecko/20100101 Firefox/10.0.12 Iceweasel/10.0.12')]
    br.open("http://3g.renren.com/album/wmyalbum.do?id=%s&sid=%s" % (
        str(frienduid), str(sid)
        ))
    outlinks = {}
    while True:
        links = br.links(url_regex=r"wgetalbum.do")
        for i in links:
            outlinks[i.url] = i.text
        lenf = 0 
        for i in br.forms():
            lenf += 1
        for i in xrange(lenf):
            k = 0
            for j in br.forms():
                br.form = j
                k += 1
                if k > i:
                    break
            br['password'] = raw_input(u'发现一个加密相册，请输入密码：')
            br.submit()
            outlinks[br.geturl()] = br.title()
            br.back()
        retry = 1
        while retry:
            retry = 0
            try:
                br.follow_link(text_regex=r"下一页", url_regex="wmyalbum.do")
            except mechanize._mechanize.LinkNotFoundError:
                return outlinks
            except Exception as e:
                retry = 1

def get_sid(username, password):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.12) Gecko/20100101 Firefox/10.0.12 Iceweasel/10.0.12')]
    resp = br.open("http://3g.renren.com/")
    for i in br.forms():
        br.form = i
        break
    html = resp.read()
    url = re.search(r'\/rndimg_wap[^"]*"', html).group(0)[:-1]
    checkcode = requests.get("http://3g.renren.com" + url).content
    img = Image.open(StringIO(checkcode))
    img.show()
    br['email'] = username
    br['password'] = password
    br['verifycode'] = raw_input(u'请输入验证码：')
    res = br.submit()
    if 'sid' in res.geturl():
        return (True, re.search('sid=([^?&]*)', res.geturl()).group(1))
    else:
        return (False, re.search(r'<div class="error">(.*?)</div>', res.read()).group(1).decode('utf-8'))
