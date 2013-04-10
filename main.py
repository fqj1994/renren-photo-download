#!/usr/bin/env python
# coding: utf-8
from user import get_album_list
from user import get_sid
from album import get_photo_list
from album import get_photo_image_url
from os import path
from os import makedirs
import sys
import locale
import requests
import getpass

reload(sys)
sys.setdefaultencoding(locale.getpreferredencoding())

requser = True

while True:
    if requser:
        requser = False
        USER = raw_input(u'用户名：')
        PASS = getpass.getpass()
    SID = get_sid(USER, PASS)
    if SID[0]:
        SID = SID[1]
        break
    else:
        if u'登录失败，请稍后重试' in SID[1]:
            pass
        else:
            requser = True
DIR = raw_input(u'请输入保存目录：')


if not path.exists(DIR):
    makedirs(DIR)

UID = raw_input(u"请输入好友ID：")

albums = get_album_list(SID, UID);
print u'共有%d个相册' % (len(albums))
for album in albums:
    print u'> 正在检查相册 %s 中的照片' % (albums[album])
    photos = get_photo_list(album)
    print u'>> 相册 %s 中共有 %d 张照片' % (albums[album], len(photos))
    if not path.exists(path.join(DIR, albums[album])):
        makedirs(path.join(DIR, albums[album]))
    for i in xrange(len(photos)):
        print u'>>> 正在下载第 %d 张照片' % (i + 1)
        url = get_photo_image_url(photos[i])
        r = requests.get(url[0])
        f = open(path.join(DIR, albums[album], '%d.%s' % (i + 1, r.url.split('.')[-1])), 'wb')
        f.write(r.content)
        f.close()
