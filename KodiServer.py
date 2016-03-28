# -*- coding: utf-8 -*-
'''
Created on 29/03/2015

@author: pybquillast

'''
import os
import urlparse
import hashlib
import webbrowser
import StringIO
import re
from functools import partial
import threading

import KodiScriptImporter as ksi

from wsgiref.simple_server import make_server

def getFile(url):
    import xbmc
    basePath, queryStr = url.split('/?', 1)
    query = urlparse.parse_qs(queryStr)
    fname, key = query['fname'][0], query['key'][0]
    basePath = xbmc.translatePath(basePath)
    fname = os.path.join(basePath, fname)
    answ = {}
    if key == hashlib.md5(open(fname, 'rb').read()).hexdigest():
        answ['Content-Type'] = 'image/' + os.path.splitext(fname)[1][1:]
        with open(fname, 'rb') as f: answ['body'] = f.read()
    else:
        answ['body'] = '<html><head><title>403 Forbidden</title></head>' \
                       '<body bgcolor="white"><br>' \
                       '<table border="0" align="center" width="720"><tr><td><h1>403 Forbidden</h1>' \
                       '<table style="border: 1px solid #f2f2f2;" bgcolor="#ffffff" align="center" width="720">' \
                       '<tr><td border="0"><tr><td><br><center><h2> server refuses to respond to request </h2>' \
                       '</center><br></td></tr></table><br><center>kodiserver</center></td></tr></table></body></html>'
        answ['Content-Type'] = 'text/html'
    return answ


def application (environ, start_response, server=None):
    url = environ.get('PATH_INFO', '')[1:] or '/'
    status = '200 OK'
    response_headers = []
    if environ.get('QUERY_STRING'):
        url += '?' + environ['QUERY_STRING']
    if url == '/' or url.startswith('plugin://'):
        response_headers.append(('Content-type', 'text/html'))
        response_body = server.runAddon(url)
    elif url.startswith('special://'):
        response = getFile(url)
        response_headers.append(('Content-type', response['Content-Type']))
        response_body = response.pop('body')
    elif url == 'file://log':
        response_headers.append(('Content-type', 'text/plain'))
        response_body = server.stEd.getvalue() or 'NOT ACTIVITY LOGGED'
    else:
        status = '404 Not Found'
        response_headers.append(('Content-type', 'text/html'))
        response_body = '<html><body><h1>Error url not in this server</h1></body></html>'
    response_headers.append(('Content-Length', str(len(response_body))))
    start_response(status, response_headers)

    return [response_body]

class KodiServer(ksi.Runner):
    htmlHead = '''<html><head><style>
        div.img {margin: 5px; border: 1px solid #ccc; float: left; width: 250px;}
        div.img:hover {border: 1px solid #777;}
        div.img img {width: 100%; height: 250px;}
        div.desc {margin-top: 10px; text-align: center; font-size: 15px; line-height: 1.0; width: 100%; height: 32px;}
        .menu {float: right; font-size: 30px;}
        </style></head><body>
        <div class="header" style="background: lime;">
        <a class="menu" href="/file://log">Log File</a>
        <h1>KodiServer</h1>
        </div>'''

    htmlTail = '''</body></html>'''

    htmlStr = '\n<div class="img">\n\t<a href="{0}">' \
              '\n\t\t<img src="{1}" alt="{2}" width="400" height="300">' \
              '\n\t\t<div class="desc">{2}</div>\n\t</a>\n</div>'

    mediaPlayer = '''
        <!doctype html>
        <head>
          <link href="http://vjs.zencdn.net/5.7.1/video-js.css" rel="stylesheet">
          <!-- If you'd like to support IE8 -->
          <script src="http://vjs.zencdn.net/ie8/1.1.2/videojs-ie8.min.js"></script>
            <style>
            .menu {float: right; font-size: 30px;}
            video.my-video {width:100%; height:100%;}
            </style>
        </head>

        <body>
    		<div class="header" style="background: lime;">
    			<a class="menu" href="/file://log">Log File</a>
    			<h1>KodiServer</h1>
    		</div>
            <videotag>
            <p class="vjs-no-js">
              To view this video please enable JavaScript, and consider upgrading to a web browser that
              <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a>
            </p>
          </video>

          <script src="http://vjs.zencdn.net/5.7.1/video.js"></script>
        </body>
        '''

    errorPage = '<html><head><title>Kodi Error</title></head><body bgcolor="white"><br>' \
                '<table border="0" align="center" width="720"><tr><td><center><h1>Kodi Error</h1></center>' \
                '<table style="border: 1px solid #f2f2f2;" bgcolor="#ffffff" align="center" width="720">' \
                '<tr><td border="0"><tr><td><br><center><h2>An error has ocurred, check the <a href="/file://log">log file</a> for more information</h2>' \
                '</center><br></td></tr></table><br><center>kodiserver</center></td></tr></table></body></html>'

    def __init__(self, importer):
        self.stEd = StringIO.StringIO()
        ksi.Runner.__init__(self, importer, self.stEd)

    def kodiAddons(self):
        import xbmc, xbmcaddon, xbmcgui
        pathDir = xbmc.translatePath('special://home/addons')
        kdAddon = {}
        for addon in os.walk(pathDir).next()[1]:
            fullpath = os.path.join(pathDir, addon, 'addon.xml')
            if not os.path.exists(fullpath): continue
            with open(fullpath, 'r') as f:
                content = f.read()
            pattern = r'<extension.+?point="xbmc.python.([^"]+)".*?/*>'
            match = re.search(pattern, content, re.DOTALL)
            if not match: continue
            atype = match.group(1)
            if atype == 'module': continue
            match = re.search('<provides>(.+?)</provides>', content)
            if atype == 'script' and not match:
                provides = ['executable']
            elif not match:
                continue
            else:
                provides = match.group(1).split(' ')
            for atype in provides:
                kdAddon.setdefault(atype, []).append(addon)

        body = ''
        for atype in ['video', 'audio', 'image', 'executable']:
            body += '<h2 style="clear:left">%s Addons</h2>' % (atype.upper())
            for addonId in sorted(kdAddon[atype]):
                kwargs = {'handle':0, 'isFolder':True, 'totalItems':0}
                addon = xbmcaddon.Addon(addonId)
                if not addon: continue
                kwargs['url'] = 'plugin://' + addonId + '/?'
                name = addon.getAddonInfo('name')
                listitem = xbmcgui.ListItem(label = name , iconImage = addon.getAddonInfo('icon'))
                listitem.setProperty('fanart_image', addon.getAddonInfo('fanart'))
                kwargs['listitem'] = listitem
                self.addDirectoryItem(**kwargs)
            self.endOfDirectory(handle = 0)
            handle, isFolder, content = self.answ
            body += self.fillListBox(content)
            self.answ = []
        return self.htmlHead + body + self.htmlTail


    def runAddon(self, url):
        if url == '/': return self.kodiAddons()
        self.run(url)
        handle, isFolder, content = self.answ
        self.answ = []
        if isFolder:
            return self.htmlHead + self.fillListBox(content) + self.htmlTail
        else:
            return self.videoPlayer(content)

    def videoPlayer(self, listitem):
        url = listitem.getProperty('path')
        iconImage = listitem.getProperty('thumbnailImage')
        videoUrl = url.split('|', 1)[0]
        videoFile = videoUrl.split('?', 1)[0]
        videoType = videoFile.rpartition('.')[2]
        if len(videoType) > 3: videoType = 'mp4'
        videoTag = '<video id="my-video" class="video-js" controls preload="auto" poster="{0}" data-setup="{1}">' \
                   '<source src="{2}" type="video/{3}">'.format(iconImage, '{}', videoUrl, videoType )
        return self.mediaPlayer.replace('<videotag>', videoTag)
        pass

    def fillListBox(self, vrtFolder):
        import xbmc
        FOLDER_DEFAULT = "http://www.graphicsfuel.com/wp-content/uploads/2012/03/folder-icon-512x512.png"
        MEDIA_DEFAULT = 'http://icons.iconarchive.com/icons/rokey/the-last-order-candy/128/media-cilp-icon.png'
        basePath = xbmc.translatePath('special://home')
        self.options = vrtFolder
        htmlPage = '<div>'
        for pos, item in enumerate(vrtFolder):
            itemLabel = item[2].getLabel()
            itemUrl = '/' + item[1] if item[3] or item[1].startswith('plugin://') else item[1]
            imtags = ['iconImage', 'thumbnailImage']
            itemIcon = ''
            for imtag in imtags:
                image = item[2].getProperty(imtag)
                if not image: continue
                if not itemIcon or image.startswith('http://') or not os.path.exists(itemIcon):
                    itemIcon = image
                if image.startswith('http://') or os.path.exists(itemIcon):break
            if itemIcon.lower() == 'defaultfolder.png': itemIcon = FOLDER_DEFAULT
            defIcon = FOLDER_DEFAULT if item[3] else MEDIA_DEFAULT
            itemIcon = itemIcon or defIcon
            if os.path.exists(itemIcon):
                if itemIcon.startswith(basePath):
                    hashval = hashlib.md5(open(itemIcon, 'rb').read()).hexdigest()
                    fpath, fname = os.path.split(itemIcon)
                    fpath = os.path.join('special://home', os.path.relpath(fpath, basePath))
                    fpath = fpath.replace('\\', '/')
                    itemIcon = '/' + fpath + '/?' + '&'.join(['fname=' + fname, 'key=' + hashval])
                else:
                    itemIcon = 'file:///' + itemIcon
            htmlPage += self.htmlStr.format(itemUrl, itemIcon, itemLabel)
        return htmlPage + '</div>'

def runServer(kodi = '', kodi_home = ''):
    importer = ksi.KodiScriptImporter(kodi, kodi_home)
    importer.install(True)
    kodiSrv = KodiServer(importer)
    wsgiApp = partial(application, server=kodiSrv)

    server_address = ('localhost', 5000)
    httpd = make_server(
        server_address[0],  # The host name
        server_address[1],  # A port number where to wait for the request
        wsgiApp  # The application object name, in this case a function
    )
    srvThread = threading.Thread(target=httpd.serve_forever)
    webbrowser.open('http://{}:{}'.format(*server_address))
    srvThread.start()
    return httpd

if __name__ == '__main__':
    runServer()
    pass

