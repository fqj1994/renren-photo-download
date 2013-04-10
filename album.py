#!/usr/bin/env python
# coding: utf-8

import mechanize

def get_photo_list(albumlink_with_sid):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.12) Gecko/20100101 Firefox/10.0.12 Iceweasel/10.0.12')]
    br.open(albumlink_with_sid)
    photos = []
    while True:
        links = br.links(url_regex=r"wgetphoto.do")
        for i in links:
            photos.append(i.url)
        retry = 1
        while retry:
            retry = 0
            try:
                br.follow_link(text_regex=r"下一页", url_regex="wgetalbum.do")
            except mechanize._mechanize.LinkNotFoundError:
                return photos
            except Exception as e:
                retry = 1

def get_photo_image_url(photolink_with_sid):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.12) Gecko/20100101 Firefox/10.0.12 Iceweasel/10.0.12')]
    br.open(photolink_with_sid)
    # 人人的图片CDN的域名太多了吧，算了不匹配URL了
    links = br.links(text_regex=r"^下载$")
    url = []
    for i in links:
        url.append(i.url)
    return list(set(url))
