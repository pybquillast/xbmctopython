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
        self.stack = []
        self.toSave = []
        self.nullstack = set()
        self.path = None
        self.pathprefix = pathprefix = 'script.module'
        self.setPaths(kodi, kodi_home)
        self.addonDir = None
        self.initRootPaths()

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
            logger.log(logging.CRITICAL, msg)
            raise ImportError(msg)

        self.path_cache = {}
        stubs = ['xbmc', 'xbmcgui', 'xbmcaddon', 'xbmcplugin', 'xbmcvfs']
        for stub in stubs:
            stubmod = os.path.join(self.KODI_STUBS, stub)
            if os.path.exists(stubmod + '.py'):
                self.path_cache[stub] = stubmod
            else:
                msg = stubmod + '.py' + " doesn't exits"
                logger.log(logging.CRITICAL, msg)
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
        pattern = r'<extension\s+point="xbmc.python.(?P<type>[^"]+)"\s+library="(?P<lib>[^"]+)"\s*/*>'
        for apath in [self.KODI, self.KODI_HOME]:
            dirs = [adir for adir in os.walk(apath).next()[1] if adir.startswith('script.module')]
            for adir in dirs:
                with open(os.path.join(apath, adir,'addon.xml'), 'r') as f:
                    content = f.read()
                atype, alib = re.findall(pattern, content)[0]
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
                return None
        elif path and (path[0].startswith(self.KODI_HOME) or path[0].startswith(self.KODI)):
            testpath = os.path.join(path[0], lastname)
        else:
            return None

        if os.path.exists(testpath) or os.path.exists(testpath + '.py'):
            logger.log(logging.INFO, 'Importing module ' + fullname)
            self.path_cache[fullname] = os.path.normpath(testpath)
            msg = 'found:' + fullname + ' at: ' + testpath
            logger.log(logging.DEBUG, msg)
            return self

        msg = 'Not found: ' + fullname
        logger.log(logging.DEBUG, msg)
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
        self.stack.append(fullname)
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
            if self.stack[0] == fullname:
                msg = '***' + fullname + '*** An error has ocurred. The following modules that were loaded before the error ocurred, are going to be unloaded: '
                logger.log(logging.DEBUG, msg)
                while self.stack:
                    key = self.stack.pop()
                    if sys.modules.has_key(key):
                        sys.modules.pop(key)
                        logger.log(logging.DEBUG, key)
            pass
        else:
            if self.stack[0] == fullname:
                logger.log(logging.INFO, 'IMPORT %s successful' % (fullname))
                if self.stack[1:]:
                    msg = 'The following modules were loaded in the process : '
                    logger.log(logging.INFO, msg)
                    for key in sorted(self.stack[1:]): logger.log(logging.INFO, key)
                    for fullname, fullpath in sorted(self.toSave):
                        self.path_cache[fullname] = os.path.splitext(fullpath)[0]
                        logger.log(logging.INFO, fullname)
                pass
        finally:
            if self.stack[0] == fullname:
                self.stack = []
            if self.nullstack:
                msg = '******The following dummy modules are going to be unloaded : *****'
                logger.log(logging.DEBUG, msg)
                toSave = []
                while self.nullstack:
                    key = self.nullstack.pop()
                    if sys.modules.has_key(key) and not sys.modules[key]:
                        rootname = key.rpartition('.')[2]
                        if sys.modules.has_key(rootname) and hasattr(sys.modules[rootname], '__file__'):
                            filename = sys.modules[rootname].__file__
                            bFlag = filename.startswith(self.KODI_HOME) or filename.startswith(self.KODI)
                            bFlag = bFlag and not self.path_cache.has_key(rootname)
                            if bFlag:
                                toSave.append((rootname, sys.modules[rootname].__file__))
                        sys.modules.pop(key)
                        logger.log(logging.DEBUG, key)
                if toSave:
                    msg = '******The following modules were created outside the KodiScriptImporter  : *****'
                    logger.log(logging.DEBUG, msg)
                    for fullname, fullpath in sorted(toSave):
                        logger.log(logging.DEBUG, fullname.ljust(15) + '  ' + fullpath)
                        self.toSave.append((fullname, fullpath))
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
            Define a logger in your __main__ script to view messages from the logging in this module
        """

        if meta_path:
            sys.meta_path.append(self)
            logger.log(logging.INFO, 'Installed as Meta Path')
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
            logger.log(logging.INFO, 'Installed as Path Hook')
        import xbmc
        logger.log(logging.INFO, 'Mapping "special://xbmc" to %s' % self.KODI)
        xbmc.special_xbmc = self.KODI
        logger.log(logging.INFO, 'Mapping "special://home" to %s' % os.path.dirname(self.KODI_HOME))
        xbmc.special_home = os.path.dirname(self.KODI_HOME)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(levelname)-6s %(message)s')
    meta_path = True
    importador = KodiScriptImporter()
    importador.install(meta_path)
    import xbmc

    import metahandler                      # @UnresolvedImport
    from metahandler import metahandlers    # @UnresolvedImport
    for obj in dir(metahandlers):
        print obj
    import urlresolver                      # @UnresolvedImport

    print urlresolver.resolve('https://www.youtube.com/watch?v=EiOglTERPEo')
