# -*- coding: utf-8 -*-
'''
Created on 29/03/2015

@author: Alex Montes Barrios

'''
import os
import sys
import urllib
import urlparse
import hashlib
import webbrowser
import logging
import StringIO
import traceback

import KodiScriptImporter

from wsgiref.simple_server import make_server

# variables
kodi = None

class newModules:
    def __init__(self, aDict):
        self.dict = aDict
        self._initKeys = aDict.keys()
    def clear(self):
        for key in self.dict.keys():
            if key in self._initKeys: continue
            self.dict.pop(key)
        pass
    def __getattr__(self, attr):
        return getattr(self.dict,attr)

class KodiFrontEnd:
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
    </div>
    <div>'''

    htmlTail = '''</div></body></html>'''

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

    def __init__(self):
        """
        Creates a new KodiFrontEnd instance.
        """
        self.kodiDirectory = []
        self.addonID = ''
        self.htmlPage = ''
        self.stEd = StringIO.StringIO()
        self.setLogger()
        self.ORIGINAL_PYTHONPATH = sys.path
        self.redefineXbmcMethods()

    def setLogger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(xbmc.LOGDEBUG+1)
        ch = logging.StreamHandler(self.stEd)
        ch.setLevel(xbmc.LOGDEBUG+1)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def initGlobals(self):
        theGlobals = {}
        exec 'import sys' in theGlobals
        theGlobals['sys'].argv = [0,0,0]
        exec 'import xbmc, xbmcgui, xbmcplugin' in theGlobals
        theGlobals["__name__"] = "__main__"
        self.theGlobals = theGlobals

    def redefineXbmcMethods(self):
        sys.modules['xbmc'].log = self.log
        sys.modules['xbmcplugin'].setResolvedUrl = self.setResolvedUrl
        sys.modules['xbmcplugin'].addDirectoryItem = self.addDirectoryItem
        sys.modules['xbmcplugin'].endOfDirectory = self.endOfDirectory

    def log(self, msg, level = 2):
        logLst = ['DEBUG', 'INFO', 'NOTICE', 'WARNING',
               'ERROR', 'SEVERE', 'FATAL', 'NONE']
        msg = '{0:>9s}:{1}'.format(logLst[level], msg)
        self.logger.log(level+1, msg)

    def setResolvedUrl(self, handle, succeeded, listitem):
        if not succeeded: return
        url = listitem.getProperty('path')
        iconImage = listitem.getProperty('thumbnailImage')
        videoUrl = url.split('|', 1)[0]
        videoFile = videoUrl.split('?', 1)[0]
        videoType = videoFile.rpartition('.')[2]
        if len(videoType) > 3: videoType = 'mp4'
        videoTag = '<video id="my-video" class="video-js" controls preload="auto" poster="{0}" data-setup="{1}">' \
                   '<source src="{2}" type="video/{3}">'.format(iconImage, '{}', videoUrl, videoType )
        self.htmlPage = self.mediaPlayer.replace('<videotag>', videoTag)
        pass


    def addDirectoryItem(self, handle, url, listitem, isFolder = False, totalItems = 0):
        kwargs = {'handle':handle, 'url':url, 'listitem':listitem, 'isFolder':isFolder, 'totalItems':totalItems}
        self.kodiDirectory.append(kwargs)

    def endOfDirectory(self, handle, succeeded = True, updateListing = False, cacheToDisc = True):
        if not succeeded: return
        options = list(self.kodiDirectory)
        self.kodiDirectory = []
        self.fillListBox(options)

    def kodiAddons(self):
        pathDir = xbmc.translatePath('special://home/addons')
        addons = [addon for addon in os.listdir(pathDir) if addon.startswith('plugin.video')]
        for addonId in sorted(addons):
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
        return self.htmlPage


    def runAddon(self, url):
        self.initGlobals()
        if url == '/': return self.kodiAddons()
        urlScheme = urlparse.urlparse(url)
        if urlScheme.scheme != 'plugin': return             # Plugin diferente
        pluginId, urlArgs = urllib.splitquery(url)
        self.theGlobals['sys'].argv = [pluginId, self.theGlobals['sys'].argv[1] + 1, '?' + (urlArgs or '')]
        self.kodiDirectory = []
        actualID = urlScheme.netloc
        addonDir = xbmc.translatePath('special://home/addons/' + actualID)
        self.addonID = actualID
        self.theGlobals['sys'].modules = newModules(self.theGlobals['sys'].modules)
        sourceCode = self.getCompiledAddonSource(actualID)
        importer.setAddonDir(addonDir)
        try:
            exec(sourceCode, self.theGlobals)
        except:
            msg = traceback.format_exc()
            self.log(msg)
            self.htmlPage = self.errorPage
        return self.htmlPage

    def getCompiledAddonSource(self, addonId):
        addon = xbmcaddon.Addon(addonId)
        path = addon.getAddonInfo('path')
        addonSourceFile = addon.getAddonInfo('library')
        addonFile = os.path.join(path, addonSourceFile)
        with open(addonFile, 'r') as f:
            addonSource = f.read()
        return compile(addonSource, addonFile, 'exec')

    def fillListBox(self, vrtFolder, selItem = 0):
        basePath = xbmc.translatePath('special://home')
        self.options = vrtFolder
        htmlPage = self.htmlHead
        for pos, item in enumerate(vrtFolder):
            itemLabel = item['listitem'].getLabel()
            itemUrl = '/' + item['url']
            imtags = ['iconImage', 'thumbnailImage']
            itemIcon = ''
            for imtag in imtags:
                image = item['listitem'].getProperty(imtag)
                if not image: continue
                if not itemIcon or image.startswith('http://') or not os.path.exists(itemIcon):
                    itemIcon = image
                if image.startswith('http://') or os.path.exists(itemIcon):break
            if itemIcon.lower() == 'defaultfolder.png': itemIcon = "http://www.graphicsfuel.com/wp-content/uploads/2012/03/folder-icon-512x512.png"
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
        self.htmlPage = htmlPage + self.htmlTail

def getFile(url):
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


def application (environ, start_response):
    url = environ.get('PATH_INFO', '')[1:] or '/'
    status = '200 OK'
    response_headers = []
    if environ.get('QUERY_STRING'):
        url += '?' + environ['QUERY_STRING']
    if url == '/' or url.startswith('plugin://'):
        response_headers.append(('Content-type', 'text/html'))
        response_body = kodi.runAddon(url)
    elif url.startswith('special://'):
        response = getFile(url)
        response_headers.append(('Content-type', response['Content-Type']))
        response_body = response.pop('body')
    elif url == 'file://log':
        response_headers.append(('Content-type', 'text/plain'))
        response_body = kodi.stEd.getvalue() or 'NOT ACTIVITY LOGGED'
    else:
        status = '404 Not Found'
        response_headers.append(('Content-type', 'text/html'))
        response_body = '<html><body><h1>Error url not in this server</h1></body></html>'
    response_headers.append(('Content-Length', str(len(response_body))))
    start_response(status, response_headers)

    return [response_body]


if __name__ == '__main__':

    importer = KodiScriptImporter.KodiScriptImporter()
    importer.install(True)
    import xbmc, xbmcgui, xbmcaddon, xbmcplugin

    kodi = KodiFrontEnd()

    server_address = ('localhost', 5000)
    httpd = make_server (
        server_address[0],  # The host name
        server_address[1],  # A port number where to wait for the request
        application         # The application object name, in this case a function
    )
    webbrowser.open('http://{}:{}'.format(*server_address))
    httpd.serve_forever()

    pass

