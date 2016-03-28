# -*- coding: utf-8 -*-
'''
Created on 9/05/2014

@author: pybquillast


'''

import sys
import os
import imp
import logging
import re
import urllib
import urlparse
import traceback

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

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
        self.stack = []
        self.indent = ''
        self.toSave = []
        self.nullstack = set()
        self.path = None
        self.pathprefix = pathprefix = 'script.module'
        self.setPaths(kodi, kodi_home)
        self.addonDir = None
        self.setLogger()
        self.initRootPaths()

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
        if os.path.exists(os.path.join(os.path.dirname(baseDirectory), 'xbmcStubs')):
            baseDirectory = os.path.join(os.path.dirname(baseDirectory), 'xbmcStubs')
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
        self.rootPaths = [self.KODI_STUBS]
        pattern = r'<extension(?P<attrib>.+?point="xbmc.python.[^"]+".*?)/*>'
        for apath in [self.KODI, self.KODI_HOME]:
            dirs = [adir for adir in os.walk(apath).next()[1] if adir.startswith('script.module')]
            for adir in dirs:
                fullname = os.path.join(apath, adir,'addon.xml')
                with open(fullname, 'r') as f:
                    content = f.read()
                try:
                    attrib = re.findall(pattern, content, re.DOTALL)[0]
                    self.log(adir + '***' + attrib, logging.INFO)
                    alib = re.findall(r'library="(?P<lib>[^"]+)"', attrib)[0]
                except Exception as e:
                    if os.path.exists(os.path.join(apath, adir, 'lib')):
                        alib = 'lib'
                        msg = 'While processing {0} an error ocurred. Defaulting the root path for module {1} to special://home/addons/{1}/lib'
                        msg = msg.format(fullname, adir, adir)
                        self.log(msg,logging.WARNING)
                    else:
                        msg = 'While processing ' + fullname + ': ' + str(e)
                        self.log(msg, logging.ERROR)
                        msg = traceback.format_exc()
                        self.log(msg, logging.ERROR)
                        continue
                root = os.path.join(apath, adir, alib)
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
        import xbmc
        self.log('Mapping "special://xbmc" to %s' % self.KODI, logging.INFO)
        xbmc.special_xbmc = self.KODI
        self.log('Mapping "special://home" to %s' % os.path.dirname(self.KODI_HOME), logging.INFO)
        xbmc.special_home = os.path.dirname(self.KODI_HOME)
        self.isInstalled = True

    def lstModules(self):
        pattern = r'<addon(?P<attrib>.+?id="placeholder".*?)>'
        retLst = []
        linf, lsup = 1, -1 if self.addonDir else len(self.rootPaths)
        for mod in self.rootPaths[linf:lsup]:
            path = os.path.dirname(mod)
            addonId = os.path.basename(path)
            fullname = os.path.join(path, 'addon.xml')
            with open(fullname, 'r') as f:
                content = f.read()
            try:
                attrib = re.findall(pattern.replace('placeholder', addonId), content, re.DOTALL)[0]
                name = re.findall(r'name="(?P<name>[^"]+)"', attrib)[0]
            except:
                pass
            retLst.append((name, addonId, os.walk(mod).next()[1]))
        return sorted(retLst)


class Runner:
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
        self.answ = []
        theGlobals = {}
        exec 'import sys' in theGlobals
        theGlobals['sys'].argv = [0,0,0]
        exec 'import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs' in theGlobals
        self.redefineXbmcMethods(theGlobals)
        theGlobals["__name__"] = "__main__"
        self.theGlobals = theGlobals

    def redefineXbmcMethods(self, theGlobals):
        theGlobals['xbmc'].log = self.log
        theGlobals['xbmcplugin'].setResolvedUrl = self.setResolvedUrl
        theGlobals['xbmcplugin'].addDirectoryItem = self.addDirectoryItem
        theGlobals['xbmcplugin'].endOfDirectory = self.endOfDirectory

    def log(self, msg, level = 2):
        logLst = ['DEBUG', 'INFO', 'NOTICE', 'WARNING',
               'ERROR', 'SEVERE', 'FATAL', 'NONE']
        if self.xbmcLoglevel < 0: return
        if self.xbmcLoglevel == 0 and level in ['DEBUG', 'INFO']: return
        msg = '{0:>9s}:{1}'.format(logLst[level], msg)
        self.logger.log(level+1, msg)

    def setResolvedUrl(self, handle, succeeded, listitem):
        if not succeeded: return
        self.answ = (handle, False, listitem)
        pass

    def addDirectoryItem(self, handle, url, listitem, isFolder = False, totalItems = 0):
        self.answ.append((handle, url, listitem, isFolder, totalItems))

    def endOfDirectory(self, handle, succeeded = True, updateListing = False, cacheToDisc = True):
        if not succeeded: return
        self.answ = (handle, True, self.answ)
        pass

    def run(self, url):
        self.initGlobals()
        xbmc = self.theGlobals['xbmc']
        urlScheme = urlparse.urlparse(url)
        if urlScheme.scheme != 'plugin': return             # Plugin diferente
        pluginId, urlArgs = urllib.splitquery(url)
        self.theGlobals['sys'].argv = [pluginId, self.theGlobals['sys'].argv[1] + 1, '?' + (urlArgs or '')]
        actualID = urlScheme.netloc
        addonDir = xbmc.translatePath('special://home/addons/' + actualID)
        self.addonID = actualID
        sourceCode = self.getCompiledAddonSource(actualID)
        self.importer.setAddonDir(addonDir)
        try:
            exec(sourceCode, self.theGlobals)
        except Exception as e:
            self.log(str(e), logging.ERROR)
            msg = traceback.format_exc()
            self.log(msg, logging.ERROR)
            self.answ = None
        return self.answ

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
    import pprint
    meta_path = True
    importador = KodiScriptImporter()
    importador.install(meta_path)
    arunner = Runner(importador)
    pprint.pprint( importador.lstModules())
    import requests
    # import bs4

    import urlresolver                      # @UnresolvedImport
    # import metahandler                      # @UnresolvedImport
    # from metahandler import metahandlers    # @UnresolvedImport
    # for obj in dir(metahandlers):
    #     print obj
    #
    # print urlresolver.resolve('https://www.youtube.com/watch?v=EiOglTERPEo')
    a, b, c = arunner.run('plugin://plugin.video.youtube/?action=play_video&videoid=EiOglTERPEo')
    print c.getProperty('path')
    pass
