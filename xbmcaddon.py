'''
Created on 9/05/2014

@author: pybquillast

This module has been ported from xbmcstubs:

__author__ = 'Team XBMC <http://xbmc.org>'
__credits__ = 'Team XBMC'
__date__ = 'Thu Apr 17 08:03:38 BST 2014'
__platform__ = 'ALL'
__version__ = '2.14.0'


'''

import sys
import os
import xbmc
import xml.etree.ElementTree as ET
import  xml.dom.minidom as minidom
import re

class Addon(object):
    def __new__(cls, *args, **kwargs):
        if args:
            addonId = args[0]
        else:
            posIni = len('plugin://')
            posFin = sys.argv[0].find('/', posIni)
            addonId = sys.argv[0][posIni:posFin]
            addonId = kwargs.get('id',addonId)
        pathDir = xbmc.translatePath('special://home/addons/' + addonId)
        addonXmlFile = os.path.join(pathDir, 'addon.xml')
        if  not os.path.exists(addonXmlFile): return False
        inst = object.__new__(cls, *args, **kwargs)
        return inst

    def __init__(self, *args, **kwargs):
        """
        --Creates a newAddon class.
        addonId : [opt] string - id of the addon as specified in addon.xml
        *Note, specifying the addon id is not needed.
        Important however is that the addon folder has the same name as the addon id provided in addon.xml.
        You can optionally specify the addon id from another installed addon to retrieve settings from it.
        example:
            - self.Addon = xbmcaddon.Addon()
            - self.Addon =xbmcaddon.Addon ('script.foo.bar')
        """
        if args:
            self.addonId = args[0]
        else:
            posIni = len('plugin://')
            posFin = sys.argv[0].find('/', posIni)
            addonId = sys.argv[0][posIni:posFin]
            self.addonId = kwargs.get('id',None) or addonId

    def getAddonInfo(self, infoId):
        """
         --Returns the value of an addon property as a string.
        infoId : string - id of the property that the module needs to access.
        *Note, choices are (author, changelog, description, disclaimer, fanart. icon, id, name, path profile, stars, summary, type, version)
        example:
            - version = self.Addon.getAddonInfo('version')
        """
        infoId = infoId.lower()
        pathDir = xbmc.translatePath('special://home/addons/' + self.addonId)
        if not os.path.exists(pathDir):
            xbmc.log('The path ' + pathDir + 'for addon ' + self.addonId + 'dosen\'t exists', xbmc.LOGFATAL)
            return ''
        if infoId in ['changelog', 'fanart', 'icon', 'path', 'profile']:
            if infoId == 'changelog': return os.path.join(pathDir, 'changelog.txt')
            elif infoId == 'fanart':  return os.path.join(pathDir, 'fanart.jpg')
            elif infoId == 'icon': return os.path.join(pathDir, 'icon.png')
            elif infoId == 'path': return pathDir
            elif infoId == 'profile': return 'special://profile/addon_data/' + self.addonId + '/'

        addonXmlFile = os.path.join(pathDir, 'addon.xml')
        if  not os.path.exists(addonXmlFile): return None
        if infoId == 'author': infoId = 'provider-name'
        attributes = ['id', 'version', 'name', 'provider-name']
        metadata = ['summary', 'description', 'disclaimer', 'platform',
                    'supportedcontent', 'language', 'license', 'forum',
                    'website', 'source', 'email']
        with open(addonXmlFile, 'r') as xmlFile:
            xmlContent = xmlFile.read()
        xmlDom = minidom.parseString(xmlContent)
        if infoId in attributes:
            heading = xmlDom.getElementsByTagName('addon')
            heading = dict(heading[0].attributes.items())
            return heading.get(infoId, None)
        elif infoId in ['type', 'library']:
            if infoId == 'type': infoId = 'point'
            heading = xmlDom.getElementsByTagName('extension')
            heading = dict(heading[0].attributes.items())
            return heading.get(infoId, None)
        elif infoId in metadata:
            metadataInfo = xmlDom.getElementsByTagName(infoId)
            if len(metadataInfo):
                return metadataInfo[0].childNodes[0].data
            return ''
        elif infoId == 'requires':
            requiresInfo = xmlDom.getElementsByTagName('import')
            modList = []
            if requiresInfo:
                for modToImport in requiresInfo:
                    modAttr = dict(modToImport.attributes.items())
                    modList.append(modAttr['addon'])
            return modList
        elif infoId == 'stars': return '0'

    def getLocalizedString(self, stringId):
        """
        --Returns an addon's localized 'unicode string'.
        stringId : integer - id# for string you want to localize.
        example:
            - locstr = self.Addon.getLocalizedString(32000)
        """
        if not isinstance(stringId, int): raise Exception('an integer is required')
        langPath = 'special://home/addons/' + self.addonId + '/resources/language/English'
        langPath = xbmc.translatePath(langPath)
        if os.path.exists(os.path.join(langPath, 'strings.xml')):
            langPath = os.path.join(langPath, 'strings.xml')
            root = ET.parse(langPath).getroot()
            srchStr = './/string[@id="%s"]' % (stringId)
            element = root.find(srchStr)
            if element is not None: return element.text
        elif os.path.exists(os.path.join(langPath, 'strings.po')):
            langPath = os.path.join(langPath, 'strings.po')
            with open(langPath, 'r') as langFile:
                langStr = langFile.read()
            pattern = r'msgctxt "#{}"\nmsgid "(?P<msgid>[^"]*)"\nmsgstr "(?P<msgstr>[^"]*)"'.format(stringId)
            match = re.search(pattern, langStr)
            if match: return match.group('msgid')
        return ''
        # raise Exception('There is no string asociated with id=' + str(stringId))

    def getSetting(self, stringId):
        """
        --Returns the value of a setting as a unicode string.
        stringId : string - id of the setting that the module needs to access.
        example:
            - apikey = self.Addon.getSetting('apikey')
        """
        settingFiles = [('value', 'special://profile/addon_data/{0}/{1}'),
                        ('default', 'special://home/addons/{0}/resources/{1}')]

        for attrId, settingXmlFile in settingFiles:
            settingXmlFile = xbmc.translatePath(settingXmlFile.format(self.addonId, 'settings.xml'))
            if not os.path.exists(settingXmlFile): continue
            root = ET.parse(settingXmlFile).getroot()
            srchStr = './/setting[@id="' + stringId + '"]'
            element = root.find(srchStr)
            if element is not None: return element.get(attrId)
        return ''

    def openSettings(self):
        """
        --Opens this scripts settings dialog.
        example:
            - self.Settings.openSettings()
        """
        pass

    def setSetting(self,settingId, value):
        """
        --Sets a script setting.
        addonId : string - id of the setting that the module needs to access. value : string or unicode - value of the setting.
        *Note, You can use the above as keywords for arguments.
        example:
            - self.Settings.setSetting(id='username', value='teamxbmc')
        """
        settingXmlFile = xbmc.translatePath('special://profile/addon_data/' + self.addonId + '/settings.xml')
        tree = ET.parse(settingXmlFile)
        root = tree.getroot()
        srchStr = './/setting[@id="' + settingId + '"]'
        element = root.find(srchStr)
        if element is None:
            element = ET.Element('setting', attrib={'id':settingId, 'value':''})
            root.append(element)
        element.set('value', str(value))
        elemList = sorted(root.getchildren(), key = lambda x: x.get('id'))
        with open(settingXmlFile, 'w') as f:
            f.write('<?xml version="1.0" ?>\n<settings>\n')
            for elem in elemList:
                setStr = '    ' + ET.tostring(elem, 'utf-8').strip() + '\n'
                f.write(setStr)
            f.write('</settings>\n')
        pass