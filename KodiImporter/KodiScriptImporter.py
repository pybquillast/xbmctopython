# -*- coding: utf-8 -*-
'''
Created on 9/05/2014

@author: pybquillast


'''

import imp
import logging
import os
import sys
import threading
import traceback
import urllib
import urlparse

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def wrapperfor(module, object):
        def wrapper(f):
            def wrapped(*args, **kwargs):
                return f(*args, **kwargs)
            wrapped.rdftag = module + '.' + object
            return wrapped
        return wrapper

class KodiScriptImporter:

    KODI_STUBS = ''
    KODI_HOME = ''
    KODI = ''
    archive = None
    prefix = ''
    path_cache = {}

    def __init__(self, kodi = '', kodi_home = ''):
        """
        Creates a new importer.

        kodi:       string - Path where the Kodi program addons was installed.
                    In windows, this default to $PROGRAMFILES/Kodi/Addons.
        kodi_home:  string - Path where the installed addons are created.
                    In Windows, this default to $APPDATA/Kodi/Addons

        Example:
            - import KodiScriptImporter as ksi
            - importer = ksi.KodiScriptImporter(kodi = r'c:/alternateKodi/Addons',
                                                kodi_home = r'c:/mykodiscrits/')
        Note:
            - For users other than Windows x86, this two variables must be explicitally set.
            - Only subdirectories that starts with 'script.module' are considered python modules
        """
        self.isInstalled = False
        self.logFilter = 0
        self.services = {}
        self.stack = []
        self.indent = ''
        self.toSave = []
        self.nullstack = set()
        self.path = None
        self.pathprefix = pathprefix = 'script.module'
        self.addonDir = None
        self.setLogger()
        self.setPaths(kodi, kodi_home)

    def setLogger(self, strLogger=None):
        self.logger = logging.getLogger('%s.importer' % (__name__))
        ch = logging.StreamHandler(strLogger)
        formatter = logging.Formatter('%(asctime)-15s %(levelname)-6s %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.setLevel(logging.INFO)

    def log(self, msg, level=2):
        if self.logFilter < 0: return
        if self.logFilter == 0 and level in [logging.INFO, logging.DEBUG]: return
        self.logger.log(level, msg)

    def setPaths(self, kodi, kodi_home):
        baseDirectory = os.path.dirname(__file__)
        if os.path.exists(os.path.join(os.path.dirname(baseDirectory), 'xbmcModules')):
            baseDirectory = os.path.join(os.path.dirname(baseDirectory), 'xbmcModules')
        self.KODI_STUBS = baseDirectory

        if sys.platform[:3] == 'win':
            kodi = kodi or os.path.join(os.path.expandvars("$PROGRAMFILES"), "Kodi", "addons")
            kodi_home = kodi_home or os.path.join(os.path.expandvars("$APPDATA"), "Kodi", "addons")
        self.KODI = kodi
        self.KODI_HOME = kodi_home

        if not all(map(os.path.exists,[self.KODI, self.KODI_HOME])):
            msg = "kodi: " + self.KODI + ' or kodi_home: ' + self.KODI_HOME + "doesn't exits"
            self.log(msg, logging.CRITICAL)
            raise ImportError(msg)

        self.path_cache = {}
        stubs = ['xbmc', 'xbmcgui', 'xbmcaddon', 'xbmcplugin', 'xbmcvfs']
        for stub in stubs:
            stubmod = os.path.join(self.KODI_STUBS, stub)
            if os.path.exists(stubmod + '.py'):
                self.path_cache[stub] = stubmod
            else:
                msg = stubmod + '.py' + " doesn't exits"
                self.log(msg, logging.CRITICAL)
                raise ImportError(msg)
        self.rootPaths = [self.KODI_STUBS]

    def setAddonDir(self, addonDir):
        if self.addonDir:
            self.rootPaths.pop()
            keys = [key for key, value in self.path_cache.items() if value.startswith(self.addonDir)]
            for akey in keys:
                self.path_cache.pop(akey)
                try:
                    sys.modules.pop(akey)
                except:
                    pass
        sys.path_importer_cache.clear()
        self.addonDir = addonDir
        self.rootPaths.append(addonDir)
        pass

    def initRootPaths(self):
        # xbmcaddon = self.load_module('xbmcaddon')
        import xbmcaddon
        moduleAddons = self.listAddonsType('xbmc.python.module')
        for addonId in moduleAddons:
            addon = xbmcaddon.Addon(addonId)
            apath = addon.getAddonInfo('path')
            alib = addon.getAddonInfo('library')
            root = os.path.join(apath, alib)
            self.rootPaths.append(root)

    def find_module(self, fullname, path = None):
        basename, sep, lastname = fullname.rpartition('.')  # @UnusedVariable
        rootname = fullname.partition('.')[0]
        testpath = self.path_cache.get(fullname, '')
        if testpath: return self
        if not path and fullname == rootname:
            for aroot in self.rootPaths:
                testpath = os.path.join(aroot, rootname)
                if os.path.exists(os.path.join(testpath, '__init__.py')) or os.path.exists(testpath + '.py'):
                    break
            else:
                if self.stack: self.stack.append(self.indent + fullname)
                return None
        elif path and (path[0].startswith(self.KODI_HOME) or path[0].startswith(self.KODI)):
            testpath = os.path.join(path[0], lastname)
        else:
            if self.stack: self.stack.append(self.indent + fullname)
            return None

        if os.path.exists(testpath) or os.path.exists(testpath + '.py'):
            self.log('Importing module ' + fullname, logging.INFO)
            self.path_cache[fullname] = os.path.normpath(testpath)
            msg = 'found:' + fullname + ' at: ' + testpath
            self.log(msg, logging.DEBUG)
            return self

        msg = 'Not found: ' + fullname
        self.log(msg, logging.DEBUG)
        self.nullstack.add(fullname)
        return

    def get_code(self,fullname):
        src = self.get_source(fullname)
        code = compile(src, self.get_filename(fullname), 'exec')
        return code

    def get_data(self, pathname):
        try:
            u = open(pathname, 'rb')
            data = u.read()
            return data
        except:
            raise ImportError("Can't find %s" % pathname)

    def get_filename(self, fullname):
        scriptPath = self.path_cache[fullname]
        if self.is_package(fullname): return os.path.join(scriptPath, '__init__.py')
        return scriptPath + '.py'

    def get_source(self, fullname):
        filename = self.get_filename(fullname)
        return self.get_data(filename)

    def is_package(self, fullname):
        fullpath = self.path_cache[fullname]
        return os.path.exists(os.path.join(fullpath, '__init__.py'))

    def load_module(self, fullname):
        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        self.stack.append(self.indent + fullname)
        self.indent += 4*' '
        mod.__file__ = self.get_filename(fullname)
        mod.__loader__ = self
        mod.__package__ = fullname.rpartition('.')[0]
        code = self.get_code(fullname)
        if self.is_package(fullname):
            mod.__package__ = fullname
            mod.__path__ = [self.path_cache[fullname]]
        try:
            exec(code, mod.__dict__)
        except:
            msg = 'An error has ocurred loading module : ' + fullname
            self.log(msg, logging.WARNING)
            self.log('The following modules will be unloaded: ', logging.WARNING)
            while 1:
                fullkey = self.stack.pop()
                key = fullkey.strip()
                if sys.modules.has_key(key):
                    sys.modules.pop(key)
                    self.log(fullkey, logging.WARNING)
                if key == fullname: break
            self.indent = fullkey.find(fullname)* ' '
            raise ImportError(msg)
        else:
            if self.stack[0] == fullname:
                self.log('IMPORT %s successful' % (fullname), logging.INFO)
                if self.stack[1:]:
                    msg = 'The following modules were loaded in the process : '
                    self.log(msg, logging.DEBUG)
                    for name in self.stack:
                        key = name.strip()
                        if not sys.modules.get(key, ''): name += ' (dummy)'
                        self.log(name, logging.DEBUG)
                pass
            else:
                self.indent = self.indent[:-4]
        finally:
            if self.stack and self.stack[0] == fullname:
                self.stack = []
                self.indent = ''
        pass
        return mod

    def install(self, meta_path = True):
        """
        Install a KodiScriptImporter instance as meta path or path hook

        meta_path:  bool - Set the instance as a META PATH importer (meta_path = True) or
                    as a PATH HOOK (meta_path = False
        Example:
            - import KodiScriptImporter as ksi
            - importer = ksi.KodiScriptImporter()           # For Windows x86 users
            - importer.install(False)                       # Install as a path hook
        Note:
            Define a self.logger in your __main__ script to view messages from the logging in this module
        """

        if meta_path:
            sys.meta_path.append(self)
            self.log('Installed as Meta Path', logging.INFO)
        else:
            class trnClass:
                def __init__(aninst, path):
                    if path == self.pathprefix:aninst.path = None
                    elif path.startswith(self.KODI_HOME) or path.startswith(self.KODI): aninst.path = [path]
                    else: raise ImportError

                def find_module(aninst, fullname, path = None):
                    return self.find_module(fullname, aninst.path)

                def __getattr__(aninst, attr):
                    return getattr(self, attr)

            sys.path_hooks.append(trnClass)
            sys.path.insert(0, self.pathprefix)
            self.log('Installed as Path Hook', logging.INFO)

        self.initRootPaths()

        import xbmc
        # from KodiAddonIDE.KodiStubs.xbmcModules import xbmc
        KODI = os.path.dirname(self.KODI)
        self.log('Mapping "special://xbmc" to %s' % KODI, logging.INFO)
        xbmc.special_xbmc = KODI
        KODI_HOME = os.path.dirname(self.KODI_HOME)
        self.log('Mapping "special://home" to %s' % KODI_HOME, logging.INFO)
        xbmc.special_home = KODI_HOME
        self.isInstalled = True
        for serviceId in self.listAddonsType('xbmc.service'):
            self.initService(serviceId)

    def listAddonsType(self, atype):
        import xbmcaddon
        answ = []
        for apath in [self.KODI, self.KODI_HOME]:
            for adir in os.walk(apath).next()[1]:
                addon = xbmcaddon.Addon(adir)
                if not addon or addon.getAddonInfo('type') != atype: continue
                answ.append(adir)
        return answ

    def listAvailable(self, atype):
        import xbmcaddon
        mapping = {'plugins': 'xbmc.python.pluginsource', 'modules':'xbmc.python.module', 'services':'xbmc.service' }
        retLst = []
        atype = mapping.get(atype, 'xbmc.python.module')
        moduleAddons = self.listAddonsType(atype)
        for addonId in moduleAddons:
            addon = xbmcaddon.Addon(addonId)
            name = addon.getAddonInfo('name')
            retLst.append((name, addonId))
        return sorted(retLst)

    def getLibraryFor(self, addonId):
        import xbmcaddon
        addon = xbmcaddon.Addon(addonId)
        apath, adir = map(addon.getAddonInfo, ['path', 'library'])
        mod = os.path.join(apath, adir)
        try:
            pckNames = os.walk(mod).next()[1]
        except:
            pckNames = []
        return pckNames

    def getServicesFor(self, addonId):
        import xbmcaddon
        retLst = []
        stack = [addonId]
        while stack:
            addonId = stack.pop()
            addon = xbmcaddon.Addon(addonId)
            if not addon: continue
            atype = addon.getAddonInfo('type')
            if atype == 'xbmc.service': retLst.append(addonId)
            requires = addon.getAddonInfo('requires')
            for req in requires:
                if req['addon'] in stack: continue
                stack.append(req['addon'])
        return retLst

    def initService(self, serviceId):
        import xbmcaddon
        servList = self.getServicesFor(serviceId)
        while servList:
            serviceId = servList.pop()
            if serviceId in self.services: continue
            addon = xbmcaddon.Addon(serviceId)
            library = addon.getAddonInfo('library')
            path = addon.getAddonInfo('path')
            addonFile = os.path.join(path, library)
            srvThread = threading.Thread(target=self.enableService, args = (serviceId, addonFile))
            # srvThread = execfile(addonFile, sys.modules['__main__'].__dict__)
            if not srvThread: continue
            self.services[serviceId] = srvThread
            srvThread.setDaemon(True)
            srvThread.setName('kodiservice_' + '_'.join(serviceId.split('.')[2:]))
            srvThread.start()
            addonXmlFile = os.path.join(path, 'addon.xml')
            root = addon._parseXml(addonXmlFile)
            element = root.find('.//extension[@point="xbmc.python.module"]')
            try:
                alib = element.attrib['library']
            except:
                pass
            else:
                alib = os.path.join(path, alib)
                if self.addonDir: self.rootPaths.insert(-1, alib)
                else: self.rootPaths.append(alib)

    def enableService(self, serviceId, addonFile):
        import xbmc
        try:
            srvThread = execfile(addonFile, sys.modules['__main__'].__dict__)
        except Exception as e:
            srvThread = None
            msg, loglevel = str(e), xbmc.LOGERROR
        else:
            msg = 'Service %s, succesfully loaded from %s'
            msg, loglevel = msg % (serviceId, addonFile), xbmc.LOGDEBUG
        finally:
            xbmc.log(msg, loglevel)
            if loglevel == xbmc.LOGERROR:
                msg = traceback.format_exc()
                xbmc.log(msg, xbmc.LOGERROR)
        return srvThread

class Runner:

    toRedef = {}

    def __init__(self, importer, strLogger=None):
        if not importer.isInstalled: importer.install()
        self.answ = []
        self.importer = importer
        self.xbmcLoglevel = 1
        self.setLogger(strLogger)

    def setLogger(self, strLogger):
        import xbmc
        self.logger = logging.getLogger('%s.runner' % (__name__))
        ch = logging.StreamHandler(strLogger)
        ch.setLevel(xbmc.LOGDEBUG + 1)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.setLevel(xbmc.LOGDEBUG + 1)

    def initGlobals(self):
        self.answ = None
        theGlobals = {}
        toExec = ['import sys',
                  'import os',
                  'import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs']
        for statement in toExec:
            exec statement in theGlobals
        theGlobals['sys'].argv = [0,0,0]
        self.redefineXbmcMethods(theGlobals)
        theGlobals["__name__"] = "__main__"
        self.theGlobals = theGlobals

    def redefineXbmcMethods(self, theGlobals):
        for method_name in dir(self):
            method = getattr(self, method_name)
            if not hasattr(method, 'rdftag'): continue
            module, obj_name = method.rdftag.rsplit('.', 1)
            module = module.split('.')
            base = theGlobals[module[0]]
            for elem in module[1:]:
                base = getattr(base, elem)
            toWrap = getattr(base, obj_name)
            if toWrap.__name__ != 'wrapper':
                setattr(base, obj_name, method(toWrap))

    @wrapperfor('xbmc', 'log')
    def log(self, func):
        def wrapper(msg, level = 2):
            logLst = ['DEBUG', 'INFO', 'NOTICE', 'WARNING',
                   'ERROR', 'SEVERE', 'FATAL', 'NONE']
            if self.xbmcLoglevel < 0: return
            if self.xbmcLoglevel == 0 and level in ['DEBUG', 'INFO']: return
            msg = '{0:>9s}:{1}'.format(logLst[level], msg)
            self.logger.log(level+1, msg)
        return wrapper

    @wrapperfor('xbmcplugin', 'setResolvedUrl')
    def setResolverUrl(self, func):
        def wrapper(handle, succeeded, listitem):
            if not succeeded: return
            self.answ = (handle, False, listitem)
        return wrapper

    @wrapperfor('xbmcplugin', 'addDirectoryItem')
    def addDirectoryItem(self, func):
        def wrapper(handle, url, listitem, isFolder = False, totalItems = 0):
            self.answ = self.answ or []
            self.answ.append((handle, url, listitem, isFolder, totalItems))
        return wrapper

    @wrapperfor('xbmcplugin', 'endOfDirectory')
    def endOfDirectory(self, func):
        def wrapper(handle, succeeded = True, updateListing = False, cacheToDisc = True):
            if not succeeded: return
            self.answ = (handle, True, self.answ)
        return wrapper

    def run(self, url):
        xbmc = self.theGlobals['xbmc']
        urlScheme = urlparse.urlparse(url)
        if urlScheme.scheme != 'plugin': return             # Plugin diferente
        pluginId, urlArgs = urllib.splitquery(url)
        self.theGlobals['sys'].argv = [pluginId, self.theGlobals['sys'].argv[1] + 1, '?' + (urlArgs or '')]
        self.addonID = actualID = urlScheme.netloc
        addonDir = xbmc.translatePath('special://home/addons/' + actualID)
        if addonDir.startswith('vrt:%s' % os.path.sep):
            self.vrtDisk.installPathHook()
            sys.path.append(addonDir)
            sourceCode = self.getVrtDiskAddonSource()
        else:
            sourceCode = self.getCompiledAddonSource(actualID)
            self.importer.setAddonDir(addonDir)
        try:
            exec(sourceCode, self.theGlobals)
        except Exception as e:
            xbmc.log(str(e), xbmc.LOGERROR)
            msg = traceback.format_exc()
            xbmc.log(msg, xbmc.LOGERROR)
            self.answ = None
        return self.answ

    def getVrtDiskAddonSource(self):
        libraryFile = self.vrtDisk.addon_library_path()
        libraryPath = 'vrt:/%s/%s' % (self.vrtDisk.addon_id(), libraryFile)
        addonSource = self.vrtDisk.getPathContent(libraryPath)
        with open(r'c:/testFiles/default.py', 'w') as f:
            f.write(addonSource.encode('utf-8'))
        return compile(addonSource.encode('utf-8'), r'c:/testFiles/default.py', 'exec')

    def getCompiledAddonSource(self, addonId):
        xbmcaddon = self.theGlobals['xbmcaddon']
        addon = xbmcaddon.Addon(addonId)
        path = addon.getAddonInfo('path')
        addonSourceFile = addon.getAddonInfo('library')
        addonFile = os.path.join(path, addonSourceFile)
        with open(addonFile, 'r') as f:
            addonSource = f.read()
        return compile(addonSource, addonFile, 'exec')


if __name__ == "__main__":
    meta_path = True
    importador = KodiScriptImporter()
    importador.install(meta_path)

    # import urlresolver
    # webMedia = urlresolver.HostedMediaFile(host='youtube.com', media_id='-j4lolWgD6Q')
    # url = webMedia.resolve()

    # arunner = Runner(importador)
    # pprint.pprint( importador.lstModules())
    # import SimpleDownloader
    # import requests
    # import bs4

    # import urlresolver                      # @UnresolvedImport
    # import metahandler                      # @UnresolvedImport
    # from metahandler import metahandlers    # @UnresolvedImport
    # for obj in dir(metahandlers):
    #     print obj
    #
    # print urlresolver.resolve('https://www.youtube.com/watch?v=EiOglTERPEo')

    # print importador.getServicesFor('script.module.simple.downloader')
    # importador.initService('script.module.simple.downloader')
    # a, b, c = arunner.run('plugin://plugin.video.youtube/?action=play_video&videoid=EiOglTERPEo')
    # url = c.getProperty('path')
    # url = 'https://r4---sn-buu-hp5l.googlevideo.com/videoplayback?sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&ip=181.49.95.60&mn=sn-buu-hp5l&sver=3&id=o-AApZxS37lQbi16dRPKNx7d3ErIMj8_z6uk0NkDFd9V56&mm=31&expire=1460025286&ms=au&mt=1460003528&mv=m&pl=22&upn=99Dq5s58WAs&itag=22&source=youtube&signature=61241BFA7BD5528EA1F4F63C8D2583AFE49FF435.98F74D1CF12D7047A3C4D00D9F776509B96DF3BD&requiressl=yes&mime=video%2Fmp4&dur=2811.750&ipbits=0&initcwndbps=432500&fexp=9416891%2C9418642%2C9419452%2C9420452%2C9422596%2C9423348%2C9423794%2C9426927%2C9427902%2C9428398%2C9431117%2C9431841%2C9431849%2C9432435%2C9433115%2C9433294%2C9433463&key=yt6&lmt=1429169029996832&ratebypass=yes'
    url = r'file:///C:/Users/Alex%20Montes%20Barrios/Pictures/Friends/Fotos%20de%20KIKI/224302_10150240242472578_5694922_n.jpg'
    filename = 'downloadertest.mp4'
    params = {'url':url,
              'download_path':'c:/testFiles/downloads'
              }
    import SimpleDownloader
    smpDwn = SimpleDownloader.SimpleDownloader()
    smpDwn.download(filename, params)  # import xbmc, xbmcaddon


    # res = xbmc.translatePath('special://skin')
    # addon = xbmcaddon.Addon('plugin.video.youtube')
    # res = addon.getAddonInfo('path')
    # res = addon.getLocalizedString(30009)
    # res = addon.getSetting('kodion.support.alternative_player')



    # arunner.run('plugin://script.common.plugin.cache/?')
    # worker = Thread(target=arunner.run, args=('plugin://script.common.plugin.cache/?',))
    # worker.start()
    pass
