import Tkinter as tk
import functools
import json
import os
import pickle
import re
import xml.etree.ElementTree as ET
from collections import deque

from xbmcModules import xbmcaddon

from KodiAddonIDE.KodiStubs.xbmcModules import xbmc
# import xbmcConstants
from KodiAddonIDE.KodiStubs.fromC.Keytable import VK, NAME, lookup
from KodiAddonIDE.KodiStubs.fromC import key as kodiKeyh, ButtonTranslator
from PIL import Image, ImageTk, ImageChops, ImageColor, ImageFont, ImageDraw

TEXTURE_DIRECTORY = 'c:/testFiles/Confluence'
IMAGECACHE_DIRECTORY = 'c:/testFiles/imagecahe'

imgCache = {}
params = {}
vars = set()

ctrClassMap = {'label': 'ControlLabel', 'button': 'ControlButton',
               'textbox': 'ControlTextBox', 'group': 'ControlGroup',
               'image': 'ControlImage', 'radiobutton': 'ControlRadioButton',
               'edit': 'ControlTextBox', 'list':'ControlList'}

coordResolution = {
                        '1080i'     : (1920, 1080), # 1080i
                        '720p'      : (1280,  720), #  720p
                        '480p  4:3' : ( 720,  480), #  480p  4:3
                        '480p 16:9' : ( 720,  480), #  480p 16:9
                        'NTSC  4:3' : ( 720,  480), #  NTSC  4:3
                        'NTSC 16:9' : ( 720,  480), #  NTSC 16:9
                        'NTSC 16:9' : ( 720,  576), #  NTSC 16:9
                        'PAL 16:9'  : ( 720,  576), #   PAL 16:9
                        'PAL60  4:3': ( 720,  480), # PAL60  4:3
                        'PAL60 16:9': ( 720,  480)  # PAL60 16:9
                    }


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(sorted(kwargs))
        if key not in cache:
            answ = obj(*args, **kwargs)
            cache[key] = pickle.dumps(answ)
        else:
            answ = pickle.loads(cache[key])
        return answ
    return memoizer

def _parseXml(settingXmlFile):
    try:
        root = ET.parse(settingXmlFile).getroot()
    except:  # ParseError
        from xml.sax.saxutils import quoteattr
        with open(settingXmlFile, 'r') as f:
            content = f.read()
            content = re.sub(r'(?<==)(["\'])(.*?)\1', lambda x: quoteattr(x.group(2)), content)
        root = ET.fromstring(content)
    return root

def _getSkinRes(xmlFilename, scriptPath, defaultSkin='Default', defaultRes='720p'):
    skinPath, skinName = xbmc.translatePath('special://skin'), xbmc.getSkinDir()
    for defRes in ['720p', 'Res']:
        fullname = os.path.join(skinPath, skinName, defRes, xmlFilename)
        if not os.path.exists(fullname): continue
        return (fullname, os.path.join(skinPath, skinName), defRes)
    else:
        fullname = os.path.join(scriptPath, defaultSkin, defaultRes, xmlFilename)
        return (fullname, os.path.join(scriptPath, defaultSkin), defaultRes)

@memoize
def getIncludeDef(includeTag, file=None):
    skinPath, skinName = xbmc.translatePath('special://skin'), xbmc.getSkinDir()
    file = file or 'includes.xml'
    filename = os.path.join(skinPath, skinName, '720p', file)     #Se debe dejar mas libre aca
    includes = _parseXml(filename)
    includeDef = includes.find('.//include[@name="%s"]' % includeTag)
    if includeDef is None and file == 'includes.xml':
        filenames = [elem.get('file') for elem in includes.findall('.//include[@file]') if elem.get('file').lower() != 'defaults.xml']
        for filename in filenames:
            filename = os.path.join(skinPath, skinName, '720p', filename)
            includes = _parseXml(filename)
            includeDef = includes.find('.//include[@name="%s"]' % includeTag)
            if includeDef is not None: break
    if includeDef is None: return includeDef, {}, set()

    paramDef = {}
    for param in includeDef.findall('.//param'):
        includeDef.remove(param)
        key, value = param.get('name'), param.get('value')
        paramDef[key] = value

    varsDef = set()
    includeStr = ET.tostring(includeDef)
    varsDef.update(elem for elem in re.findall(r'\$VAR\[(.+?)\]', includeStr))
    includeDef = ET.fromstring(includeStr)
    return includeDef, paramDef, varsDef

def getAnimation(properties, animElem):
    animation = properties.setdefault('animation', {})
    tipo = animElem.get('type') if len(animElem) else animElem.text
    effect = animation.setdefault(tipo, [])
    effect.append(animElem.attrib)
    for anEffect in animElem:
        effect.append(anEffect.attrib)
    return properties

def getProperties(properties, ctrElem):
    key = ctrElem.tag
    value = ctrElem.text
    if ctrElem.attrib:
        map = dict(ctrElem.attrib)
        map['value'] = value
        properties[key] = map
    else:
        properties[key] = value
    return properties

def processElem(controlElem, toProcess, properties):
    masterId = controlElem.get('MASTERID', None) if controlElem.tag == 'include' else controlElem.get('ID', None)
    for elem in controlElem.getchildren():
        if elem.tag == 'animation':
            properties = getAnimation(properties, elem)
            continue
        if len(elem) > 0 or elem.tag in ['control', 'include']:
            elem.set('MASTERID', masterId)
            toProcess.append(elem)
        else:
            properties = getProperties(properties, elem)
    if properties: properties['MASTERID'] = properties.get('MASTERID', masterId)
    return toProcess, properties


def getIncludes(includeElem):
    def evalCondition(condition):
        return False if condition else True
    global params, vars
    inParams = params or {}
    inVars = vars or set()
    condition = includeElem.get('condition')
    if not evalCondition(condition): return [], {}
    includeTag = includeElem.get('name') or includeElem.text
    includeDef, outParam, outVars = getIncludeDef(includeTag, file=includeElem.get('file', None))
    if includeDef is None: return [], {}

    for param in includeElem.findall('.//param'):
        key, value = param.get('name'), param.get('value') or param.text or param.get('default')
        inParams[key] = value
    outParam.update(inParams)
    params = outParam

    vars = outVars.union(inVars)
    includeDef.set('MASTERID', includeElem.get('MASTERID', None))
    toProcess, properties = processElem(includeDef, [], {})
    return toProcess, properties

@memoize
def getDefaultFor(ctrType):
    skinPath, skinName = xbmc.translatePath('special://skin'), xbmc.getSkinDir()
    filename = os.path.join(skinPath, skinName, '720p', 'defaults.xml')     #Se debe dejar mas libre aca
    includes = _parseXml(filename)
    controlDef = includes.find('.//default[@type="%s"]' % ctrType)
    if controlDef is None: return {}
    ctrMap = {'type': ctrType}
    for elem in controlDef:
        ctrMap = getProperties(ctrMap, elem)
    return ctrMap

def getControl(control):
    if control.tag == 'control':
        ctrType = control.get('type')
        properties = getDefaultFor(ctrType)
    else:
        properties = {}
    properties['elem_tag'] = control.tag
    toProcess = []

    if len(control) > 0:
        properties.update(control.attrib)
        toProcess, properties = processElem(control, toProcess, properties)
    else:
        properties = getProperties(properties, control)
    return toProcess, properties

def normParams(wndStr, params):
    if params:
        newStr = ''
        while True:  # to capture parameter forwarding
            newStr = re.sub(r'\$PARAM\[(.+?)\]',lambda x: params[x.group(1)], wndStr)
            if newStr == wndStr: break
            wndStr = newStr
    return wndStr

def normVars(wndStr, varSet):
    def evCondition(condition):
        return False
    skinPath, skinName = xbmc.translatePath('special://skin'), xbmc.getSkinDir()
    filename = os.path.join(skinPath, skinName, '720p', 'includes.xml')     #Se debe dejar mas libre aca
    includes = _parseXml(filename)
    params = {}
    for var in varSet:
        variable = includes.find('.//variable[@name="%s"]' % var)
        for cond in variable.findall('.//value[@condition]'):
            variable.remove(cond)
            condition = cond.get('condition')
            if not evCondition(condition): continue
            params[var] = cond.text
            break
        else:
            cond = variable.find('.//value')
            params[var] = cond.text
    if params:
        wndStr = re.sub(r'\$VAR\[(.+?)\]', lambda x: params[x.group(1)], wndStr)
    return wndStr

def addonStr(addonId, strId):
    addon = xbmcaddon.Addon(addonId)
    return addon.getLocalizedString(int(strId))

def normLocStr(wndStr):                 # http://kodi.wiki/view/Label_Parsing
    def calcInfo(infolabel):
        return infolabel.lower()        # must be the calculated infolabel
    def pinfo(infolabel, prefix, postfix):
        infolabel = calcInfo(infolabel)
        prefix = prefix or ''
        postfix = postfix or ''
        if infolabel:
            return prefix.replace('$COMMA', ',').replace('$$', '$') + infolabel + postfix.replace('$COMMA', ',').replace('$$', '$')
        return ''

    for pattern, lambdaFunc in [(r'\$LOCALIZE\[(.+?)\]', lambda x: params[x.group(1)]),
                                (r'"label": "([0-9]+)"', lambda x: '"label": "%s"' % params[x.group(1)])]:
        params = re.findall(pattern, wndStr)
        if params:
            addon = xbmcaddon.Addon('resource.language.en_gb')
            lstr = [addon.getLocalizedString(int(locstr)) for locstr in params]
            params = dict(zip(params, lstr))
            wndStr = re.sub(pattern, lambdaFunc, wndStr)

    if '$ADDON[' in wndStr:
        wndStr = re.sub(r"\$ADDON\[([^ ]+) (.+?)\]",
                        lambda x: addonStr(x.group(1), x.group(2)),
                        wndStr)

    if '$INFO[' in wndStr:
        wndStr = re.sub(r"\$INFO\[([^,\]]+)(?:,([^,\]]*)(?:,([^,]*))*)*\]",
                        lambda x: pinfo(x.group(1), x.group(2), x.group(3)),
                        wndStr)
    return wndStr

def getRoots(xmlFilename, scriptPath, defaultSkin='Default', defaultRes='720p'):
    filename = _getSkinRes(xmlFilename, scriptPath, defaultSkin=defaultSkin, defaultRes=defaultRes)[0]
    window = _parseXml(filename)
    controls = window.find('controls')
    window.remove(controls)
    return window, controls

def processMasterFor(childID, masterID, ctrList):
    chldMap = ctrList[childID]
    mstrMap = ctrList[masterID]
    children = mstrMap.setdefault('CHILDREN', [])
    children.append(childID)
    pass

def processRoot(controls):
    global params, vars
    stack = deque()
    stack.append(deque([controls]))
    mapTab = {}
    ctrList = []
    params = {}
    vars = set()
    while stack:
        controlSet = stack.popleft()
        while controlSet:
            control = controlSet.popleft()
            if control.tag in ['controls', 'definition']:
                toProcess = []
                properties = {}
                if control.attrib: properties.update(control.attrib)
                ctrId = control.get('MASTERID', None)
                for elem in control.getchildren():
                    elem.set('MASTERID', ctrId)
                    toProcess.append(elem)
            elif control.tag == 'include':
                toProcess, properties = getIncludes(control)
                pass
            elif len(control) > 0:
                defId = str(len(ctrList))
                control.set('ID', defId)
                toProcess, properties = getControl(control)
            if properties:
                if properties.get('ID', '-') != '-':
                    id = properties.get('ID')
                    mapTab[id] = len(ctrList)
                    ctrList.append(dict(properties))
                    # print ctrList[-1]
                    masterId = properties.get('MASTERID')
                    if masterId and masterId != '-':
                        processMasterFor(mapTab[id], mapTab[masterId], ctrList)
                elif properties.get('MASTERID', '-') != '-':
                    id = properties.pop('MASTERID')
                    nPos = mapTab[id]
                    if 'animation' not in ctrList[nPos]:
                        ctrList[nPos].update(properties)
                    else:
                        animation = properties.pop('animation')
                        ctrList[nPos].update(properties)
                        animMap = ctrList[nPos].setdefault('animation', {})
                        animMap.update(animation)
                else:
                    ctrList.append(dict(properties))
            if toProcess:
                if controlSet: stack.appendleft(controlSet)
                controlSet = deque(toProcess)
                # break
    wndStr = json.dumps(ctrList)
    wndStr = normParams(wndStr, params)
    wndStr = normVars(wndStr, vars)
    wndStr = normLocStr(wndStr)
    wndStr = re.sub(r'"(-?[0-9]+)"',lambda x: x.group(1), wndStr)
    ctrList = json.loads(wndStr)
    return ctrList


def normControlMap(ctrList, scrResW, scrResH):
    grpList = [None]
    rootgrp = []
    for k, elem in enumerate(ctrList):
        if elem['elem_tag'] != 'control': continue
        if elem['MASTERID'] is None: rootgrp.append(k)
        if elem['type'] == 'grouplist':
            itemgap = elem.pop('itemgap')
            orientation = elem.pop('orientation')
            if orientation == 'horizontal':
                pos1, pos2 = 'left', 'top'
                dir1, dir2 = 'left', 'right'
                dim1, dim2 = 'width', 'height'
            else:
                pos1, pos2 = 'top', 'left'
                dir1, dir2 = 'up', 'down'
                dim1, dim2 = 'height', 'width'
            children = elem.pop('CHILDREN')
            width = 0
            height = 0
            frst = None
            last = None
            for chpos in children:
                ctr = ctrList[chpos]
                frst = frst or ctr
                last = last or ctr
                ctr[pos1] = width
                ctr[pos2] = 0
                width += ctr[dim1] + itemgap
                height = max(height, ctr[dim2])
                ctr['on' + dir1] = last['id']
                last['on' + dir2] = ctr['id']
                last = ctr
            last['on' + dir2] = frst['id']
            frst['on' + dir1] = last['id']
            elem[dim1] = width
            elem[dim2] = height
            elem['type'] = 'group'
        else:
            masterPos = elem['MASTERID']
            if masterPos is None:
                masterW, masterH = scrResW, scrResH
            else:
                master = ctrList[masterPos]
                masterW, masterH = master['width'], master['height']

            if elem['type'] == 'group':
                grpList.append((k, elem.pop('CHILDREN', [])))
        getPosAndDim(elem, scrResW, scrResH)

    grpList[0] = (None, rootgrp)
    while grpList:
        aPos, children = grpList.pop()
        x1 = y1 = x2 = y2 = 0
        for childPos in children:
            ctr = ctrList[childPos]
            x1 = min(x1, ctr['left'])
            y1 = min(y1, ctr['top'])
            x2 = max(x2, ctr['left'] + ctr['width'])
            y2 = max(y2, ctr['top'] + ctr['height'])
        if aPos is not None:
            ctrList[aPos]['width'] = x2 - x1
            ctrList[aPos]['height'] = y2 - y1

    return x2 - x1, y2 - y1

def getLabelKwd(ctrTags):
    LBLTAGS = ['label', 'info', 'number']
    lblkey = set(LBLTAGS).intersection(ctrTags.keys())
    if not lblkey: return ''
    lblkey = lblkey.pop()
    lblTag = ctrTags.pop(lblkey)
    if lblkey == 'label':
        try:
            int(lblTag)
        except:
            label = normLocStr(lblTag)
        else:
            label = addonStr('resource.language.en_gb', lblTag)
    elif lblkey == 'number':
        label = str(lblTag)
    elif lblkey == 'info':
        label = lblTag  # Debe ser el valor pedido por el infolabel
    else:
        label = ''
    return label

def getAlignKwd(ctrTags):
    alignMap = {'left': 0x00000000, 'right': 0x00000001, 'center': 0x00000002,
                'top': 0x00000000, 'centery': 0x00000004}
    alignx = ctrTags.get('align', 'left')
    aligny = 'centery' if ctrTags.get('aligny') == 'center' else 'top'
    align = alignMap[alignx] | alignMap[aligny]
    return align

def getOtherKwd(ctrTags, keys):
    equiv = {'textcolor':'textColor', 'texture':'filename',
             'texturefocus':'focusTexture', 'texturenofocus':'noFocusTexture',
             'textoffsetx':'textOffsetX', 'textoffsety':'textOffsetY',
             'focusedcolor':'focusedColor', 'disabledcolor':'disabledColor',
             'shadowcolor':'shadowColor',
             'colorkey':'colorKey', 'aspectratio':'aspectRatio', 'colordiffuse':'colorDiffuse'}
    for key in set(['texture', 'texturefocus', 'texturenofocus']).intersection(keys):
        if isinstance(ctrTags[key], dict):
            ctrTags[key] = ctrTags[key]['value']
        ctrTags[key] = os.path.join(r'C:\testFiles\Confluence',ctrTags[key])

    answ = {}
    for key in keys:
        ekey = key
        if equiv.has_key(key):
            ekey = equiv[key]
        answ[ekey] = ctrTags[key]
    return answ

# def mapControl(ctrMap, masterW, masterH):
def mapControl(ctrPos, ctrList):

    def normTexture(texture):
        if isinstance(texture, basestring):
            texture = dict(border=5, value=texture)
        return texture

    ctrMap = ctrList[ctrPos].copy()

    NAVTAGS   = ['onup', 'ondown', 'onleft', 'onright', 'onback']
    FNCTAGS   = ['oninfo', 'onclick', 'onfocus', 'onunfocus']
    STATETAGS = ['enable', 'visible']
    RELATIONALTAGS = [NAVTAGS, FNCTAGS, STATETAGS]

    notImplemented = ['hitrect', 'pulseonselect', 'animation', 'camera', 'depth',
                      'description', 'scrolltime', 'autoscroll', 'pagecontrol',
                      'pulseonselect']

    BASICTAGS = ['type', 'id']
    toClean = ['ID', 'elem_tag']


    # getPosAndDim(masterW, masterH, ctrMap)

    args = map(ctrMap.pop, ['left', 'top', 'width', 'height'])

    relationalTags = {}
    for tagkey, relTag in zip(['navtags', 'fnctags', 'statetags'], RELATIONALTAGS):
        tags = {}
        for key in set(relTag).intersection(ctrMap.keys()):
            tags[key] = ctrMap.pop(key)
        relationalTags[tagkey] = tags

    for key in set(toClean + notImplemented).intersection(ctrMap.keys()):
        ctrMap.pop(key)

    _params = dict(master=ctrMap.pop('MASTERID', None))
    id = ctrMap.pop('id', None)
    if id: _params['id'] = id

    type = ctrMap.pop('type')
    controlClass = ctrClassMap.get(type, type)
    kwargs = {}
    if type == 'image':
        ctrMap['type'] = 'image'

        texture = normTexture(ctrMap.pop('texture'))
        filename = texture['value']
        args.append(filename)

        texture['value'] = 'item.texture'
        ctrMap['texture'] = texture

        colorDiffuse = ctrMap.pop('colordiffuse', None)
        ctrMap['colordiffuse'] = 'item.colordiffuse'
        kwargs['colorDiffuse'] = colorDiffuse

        _params['layout'] = ctrMap

    elif type == 'label':
        ctrMap['type'] = 'label'

        label = ctrMap.pop('label', '')
        args.append(label)
        ctrMap['label'] = 'item.label'

        textColor, disabledColor = ctrMap.pop('textcolor', None), ctrMap.pop('disabledcolor', None)
        kwargs['textColor'] = textColor
        kwargs['disabledColor'] = disabledColor

        _params['layout'] = ctrMap

    elif type in ['button', 'radiobutton']:
        texturefocus = normTexture(ctrMap.pop('texturefocus', None))
        _params['focusTxure'] = dict(aspectratio='stretch', texture=texturefocus, type='image')

        texturenofocus = normTexture(ctrMap.pop('texturenofocus', None))
        _params['nofocusTxure'] = dict(aspectratio='stretch', texture=texturenofocus, type='image')

        vars = ['label', 'shadowColor', 'font', 'textColor', 'focusedColor', 'disabledColor']
        for key in vars:
            lkey = key.lower()
            kwargs[key] = ctrMap.pop(lkey, None)
            ctrMap[lkey] = 'item.%s' % lkey

        if type == 'radiobutton':
            vars = [('textureradioonfocus', 'focusOnTexture'),
                    ('textureradioonnofocus', 'noFocusOnTexture'),
                    ('textureradioofffocus', 'focusOffTexture'),
                    ('textureradiooffnofocus', 'noFocusOffTexture')]
            for key1, key2 in vars:
                kwargs[key2] = ctrMap.pop(key1, None)
            for key in ['radioposx', 'radioposy', 'radiowidth', 'radioheight']:
                value = ctrMap.pop(key, None)
                if value: _params[key] = value

        ctrMap['type'] = 'label'
        _params['lbllayout'] = ctrMap

    elif type == 'textbox':
        ctrMap['type'] = 'label'
        text = ctrMap.pop('label', '')
        ctrMap['label'] = 'item.label'
        _params['text'] = text
        _params['layout'] = ctrMap
    elif type == 'list':
        layouts = ctrMap['CHILDREN']
        _itemHeight = 0
        for layoutPos in layouts:
            layout = ctrList[layoutPos]
            _itemHeight = max(_itemHeight, layout['height'])
            key = layout['elem_tag']
            children = layout['CHILDREN']
            for k, childPos in enumerate(children):
                children[k] = ctrList[childPos].copy()
                for tag in ['MASTERID', 'ID', 'elem_tag']:
                    children[k].pop(tag, None)
                ctrList[childPos]['elem_tag'] = 'layoutitem'
            _params[key] = children
        kwargs['_itemHeight'] = _itemHeight
        pass

    kwargs['_params'] = _params
    return controlClass, args, kwargs, relationalTags


def mapArgsKwargs(ctrList, nPos):
    ctrTags = ctrList[nPos]

    GENTAGS = ['description', 'type', 'id', 'visible', 'animation',
               'camera', 'depth', 'colordifuse',
               'onback', 'oninfo', 'onfocus', 'onunfocus',
               'hitrect', 'enable', 'pulseonselect', 'CHILDREN']

    genTags = {}
    for key in set(GENTAGS).intersection(ctrTags.keys()):
        genTags[key] = ctrTags.pop(key)

    ctype = genTags['type']
    genTags['ctrClass'] = ctrClassMap.get(ctype, ctype)

    args = []
    POSTAGS = ['posx', 'posy', 'left', 'right', 'top', 'bottom',
               'centerleft', 'centerright', 'centertop', 'centerbottom',
               'height', 'width']
    posTags = {}
    for key in set(POSTAGS).intersection(ctrTags.keys()):
        posTags[key] = ctrTags.pop(key)

    width = int(posTags.get('width', 0))
    height = int(posTags.get('height', 0))

    get = posTags.get
    x = get('posx') or get('left') or (int(get('right')) - width if get('right') is not None else None)
    if x is None:
        if   get('centerleft') is not None:
            x = get('centerleft') - width/2
        elif get('centerright') is not None:
            x = get('centerright') + width/2
        else:
            x = 0
    else:
        if x[-1] == 'r':
            masterId =  ctrTags.get('MASTERID', None)
            if masterId is None:
                mwidth = 300
            else:
                mwidth = ctrList[int(masterId)]['width']
            x = int(mwidth) - int(x)
        else:
            x = int(x)


    y = get('posy') or get('top') or (int(get('bottom')) + height if get('bottom') is not None else None)
    if y is None:
        if get('centertop') is not None:
            y = get('centertop') - height/2
        elif get('centerbottom') is not None:
            y = get('centerbottom') + height/2
        else:
            y = 0
    else:
        if y[-1] == 'r':
            masterId =  ctrTags.get('MASTERID', None)
            if masterId is None:
                mheight = 300
            else:
                mheight = ctrList[int(masterId)]['height']
            y = int(mheight) - int(y)
        else:
            y = int(y)

    args = [x, y, width, height]

    NAVTAGS = ['onup', 'ondown', 'onleft', 'onright']

    navTags = {}
    for key in set(NAVTAGS).intersection(ctrTags.keys()):
        navTags[key] = ctrTags.pop(key)

    kwargs = {}
    if genTags['type'] == 'label':
        args.append(getLabelKwd(ctrTags))
        kwargs['_alignment'] = getAlignKwd(ctrTags)
        otherkwds = set(['angle', 'haspath', 'font', 'textcolor']).intersection(ctrTags)
        kwargs.update(getOtherKwd(ctrTags, otherkwds))
    elif genTags['type'] == 'button':
        args.append(getLabelKwd(ctrTags))
        kwargs['alignment'] = getAlignKwd(ctrTags)
        otherkwds = set(['texturefocus', 'texturenofocus',
                         'font', 'textcolor',
                         'focusedcolor', 'disabledcolor', 'shadowcolor',
                         'angle', 'textoffsetx', 'textoffsety']).intersection(ctrTags)
        kwargs.update(getOtherKwd(ctrTags, otherkwds))
    elif genTags['type'] == 'image':
        otherkwds = set(['texture', 'aspectratio']).intersection(ctrTags)
        kwargs.update(getOtherKwd(ctrTags, otherkwds))
        texture = kwargs.pop('filename')
        args.append(texture)
    elif genTags['type'] in ['textbox', 'edit']:
        otherkwds = set(['font', 'textcolor']).intersection(ctrTags)
        kwargs.update(getOtherKwd(ctrTags, otherkwds))
    elif genTags['type'] == 'group':
        pass
    elif genTags['type'] == 'radiobutton':
        args.append(getLabelKwd(ctrTags))
        kwargs['_alignment'] = getAlignKwd(ctrTags)
        otherkwds = ['texturefocus', 'texturenofocus', 'font', 'textcolor',
                     'focusedcolor', 'disabledcolor', 'shadowcolor',
                     'textoffsetx', 'textoffsety']

        otherkwds = set(otherkwds).intersection(ctrTags)
        kwargs.update(getOtherKwd(ctrTags, otherkwds))
    elif genTags['type'] == 'grouplist':
        childrenPos = genTags['CHILDREN']
        adim, odim = ('width', 'height') if ctrTags['orientation'] == 'horizontal' else ('height', 'width')
        args = dict(zip(['x', 'y', 'width', 'height'], args))
        gap = ctrTags.get('itemgap', 5)
        args[adim] = -gap
        for chldpos in childrenPos:
            chldMap = ctrList[chldpos]
            args[adim] += gap + chldMap.get(adim, 0)
            args[odim] = max(args[odim], chldMap.get(odim, 0))
        args = [args[key] for key in ['x', 'y', 'width', 'height']]
        genTags['ctrClass'] = ctrClassMap['group']
    elif genTags['type'] == '':
        x, y, width, height = args
        # Here must me set to the values for the active screen resolution
        if width is None:
            width = 500 - x
        if height is None:
            height = 600 - y
        args = [x, y, width, height]


    return genTags, args, kwargs, navTags

class AppAction:
    def __init__(self, id, buttoncode=0, amnt1=1.0, amnt2=0.0):
        self._id = id
        self._buttoncode = buttoncode
        self._amnt1 = amnt1
        self._amnt2 = amnt2
    def getId(self):
        return self._id
    def getButtonCode(self):
        return self._buttoncode
    def getAmount1(self):
        return self._amnt1
    def getAmount2(self):
        return self._amnt2


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AppWindow(tk.Tk, object):
    __metaclass__ = Singleton
    def __init__(self):
        tk.Tk.__init__(self)
        self.onInit()

    def _wndattr(self):
        wdgid, wdgname = self.mapped[-1]
        wdg = self.nametowidget(wdgid)
        return wdg, wdgname


    def onInit(self):
        self.mapped = []
        self.unmapped  = []
        self._mouseX = 0
        self._mouseY = 0
        self._mouseT = 0
        self._mouseState = ''
        # self.bind('<FocusIn>', self.focusIn)
        # self.bind_all('<Key>', self.onKey)
        # self.event_add('<<mouseaction>>', '<Button>', '<ButtonRelease>',
        #                '<Motion>', '<MouseWheel>')
        # self.bind_all('<<mouseaction>>', self.onMouse)
        self.bind_all('<Map>', self.onMap)
        self.bind_all('<Unmap>', self.onUnmap)

    def onStudy(self, event):
        self.printEvent(event)

    def onKey(self, event):
        key = event.keysym_num
        if 65 <= key <= 90: key += 32
        btnCode = key
        id = None
        keyName = lookup(key, VK)
        if keyName is not None:
            keysym = keyName[NAME]
        else:
            id = key
            keysym = 'key'
        # keymod = {'ctrl':0x0004,'shift':0x0001|0x0002,'alt':0x0008|0x0080}
        keymod = {'ctrl':0x0004,'shift':0x0001|0x0002,'alt':0x0080}
        mod = []
        for key in keymod:
            if event.state & keymod[key]:
                mod.append(key)
        mod = ','.join(mod)
        wdg, wdgname = self._wndattr()
        actionId = getActionFor(keysym, id, mod, 'keyboard', windowsname=wdgname)
        # if btnCode <= 256 and actionId == kodiKeyh.ACTION_NONE: return
        note = AppAction(actionId, buttoncode=btnCode)
        wdg.onAction(note)

    def onMouse(self, event):
        key = ''
        id = None
        if event.num in [4,5]:
            key = 'wheelup' if event.num == 4 else 'wheeldown'
        if event.type == '4':
            deltaT = abs(event.time - self._mouseT)
            if deltaT < 200:
                key = 'doubleclick'
                id = event.num - 1
                self._mouseState = key
            self._mouseX = event.x_root
            self._mouseY = event.y_root
            self._mouseT = event.time
        elif event.type == '5':
            deltaX = abs(self._mouseX - event.x_root)
            deltaY = abs(self._mouseY - event.y_root)
            if deltaX < 5 and deltaY < 5:
                deltaT = abs(event.time - self._mouseT)
                if deltaT < 1000:
                    if self._mouseState != 'doubleclick':
                        key = ['leftclick', 'middleclick', 'rightclick'][event.num - 1]
                else:
                    key = 'longclick'
                    id = event.num - 1
            else:
                key = self._mouseState + 'end'
            self._mouseT = event.time
            self._mouseX = self._mouseY = 0
            self._mouseState = ''
        elif event.type == '6':
            deltaX = abs(self._mouseX - event.x_root)
            deltaY = abs(self._mouseY - event.y_root)
            if deltaX > 5 or deltaY > 5:
                key = 'mousemove'
                if event.state & 0x0100:
                    key = 'mousedrag'
                elif event.state & 0x0400:
                    key = 'mouserdrag'
                if key != 'mousemove' and self._mouseState != key:
                    self._mouseState = key
                    key = key + 'start'

        elif event.type == '38':
            key = 'wheelup' if event.delta > 0 else 'wheeldown'
        if not key: return
        wdg, wdgname = self._wndattr()
        actionId = getActionFor(key, id, device='mouse', windowsname=wdgname)
        # note = AppAction(actionId,amnt1=1.0*event.x_root, amnt2=1.0*event.y_root)
        # abajo only for test
        note = AppAction(actionId, buttoncode=key,amnt1=1.0*event.x_root, amnt2=1.0*event.y_root)
        wdg.onAction(note)

    def onMap(self, event):
        if isinstance(event.widget, tk.Toplevel):
            wdg = event.widget
            wdgName = getattr(wdg, 'windowname', None)
            self.mapped.append((wdg.winfo_name(), wdgName))
            print '\n<Map> ' + str(event.widget.__class__) + '\n'
            # self.printEvent(event)

    def onUnmap(self, event):
        if isinstance(event.widget, tk.Toplevel):
            ctrl = str(event.widget)
            self.mapped.pop()
            self.unmapped.append(ctrl)
            print '\n<Unmap> ' + str(event.widget.__class__) + '\n'
            self.printEvent(event)




class AppWindowOLD(tk.Tk, object):
    __metaclass__ = Singleton
    def __init__(self):
        tk.Tk.__init__(self)
        self.onInit()

    def _wndattr(self):
        wdgid, wdgname = self.mapped[-1]
        wdg = self.nametowidget(wdgid)
        return wdg, wdgname


    def onInit(self):
        self.mapped = []
        self.unmapped  = []
        self._mouseX = 0
        self._mouseY = 0
        self._mouseT = 0
        self._mouseState = ''
        self.bind('<FocusIn>', self.focusIn)
        self.bind_all('<Key>', self.onKey)
        self.event_add('<<mouseaction>>', '<Button>', '<ButtonRelease>',
                       '<Motion>', '<MouseWheel>')
        self.bind_all('<<mouseaction>>', self.onMouse)
        self.bind_all('<Map>', self.onMap)
        self.bind_all('<Unmap>', self.onUnmap)

    def onStudy(self, event):
        self.printEvent(event)

    def onKey(self, event):
        key = event.keysym_num
        if 65 <= key <= 90: key += 32
        btnCode = key
        id = None
        keyName = lookup(key, VK)
        if keyName is not None:
            keysym = keyName[NAME]
        else:
            id = key
            keysym = 'key'
        # keymod = {'ctrl':0x0004,'shift':0x0001|0x0002,'alt':0x0008|0x0080}
        keymod = {'ctrl':0x0004,'shift':0x0001|0x0002,'alt':0x0080}
        mod = []
        for key in keymod:
            if event.state & keymod[key]:
                mod.append(key)
        mod = ','.join(mod)
        wdg, wdgname = self._wndattr()
        actionId = getActionFor(keysym, id, mod, 'keyboard', windowsname=wdgname)
        # if btnCode <= 256 and actionId == kodiKeyh.ACTION_NONE: return
        note = AppAction(actionId, buttoncode=btnCode)
        wdg.onAction(note)

    def onMouse(self, event):
        key = ''
        id = None
        if event.num in [4,5]:
            key = 'wheelup' if event.num == 4 else 'wheeldown'
        if event.type == '4':
            deltaT = abs(event.time - self._mouseT)
            if deltaT < 200:
                key = 'doubleclick'
                id = event.num - 1
                self._mouseState = key
            self._mouseX = event.x_root
            self._mouseY = event.y_root
            self._mouseT = event.time
        elif event.type == '5':
            deltaX = abs(self._mouseX - event.x_root)
            deltaY = abs(self._mouseY - event.y_root)
            if deltaX < 5 and deltaY < 5:
                deltaT = abs(event.time - self._mouseT)
                if deltaT < 1000:
                    if self._mouseState != 'doubleclick':
                        key = ['leftclick', 'middleclick', 'rightclick'][event.num - 1]
                else:
                    key = 'longclick'
                    id = event.num - 1
            else:
                key = self._mouseState + 'end'
            self._mouseT = event.time
            self._mouseX = self._mouseY = 0
            self._mouseState = ''
        elif event.type == '6':
            deltaX = abs(self._mouseX - event.x_root)
            deltaY = abs(self._mouseY - event.y_root)
            if deltaX > 5 or deltaY > 5:
                key = 'mousemove'
                if event.state & 0x0100:
                    key = 'mousedrag'
                elif event.state & 0x0400:
                    key = 'mouserdrag'
                if key != 'mousemove' and self._mouseState != key:
                    self._mouseState = key
                    key = key + 'start'

        elif event.type == '38':
            key = 'wheelup' if event.delta > 0 else 'wheeldown'
        if not key: return
        wdg, wdgname = self._wndattr()
        actionId = getActionFor(key, id, device='mouse', windowsname=wdgname)
        # note = AppAction(actionId,amnt1=1.0*event.x_root, amnt2=1.0*event.y_root)
        # abajo only for test
        note = AppAction(actionId, buttoncode=key,amnt1=1.0*event.x_root, amnt2=1.0*event.y_root)
        wdg.onAction(note)

    def focusIn(self, event):
        if self.mapped:
            wdgName = self.mapped[-1]
            wdg = self.nametowidget(wdgName)
            wdg.focus_set()
            wdg.lift()


    def printEvent(self, event):
        print 70*'=' + '\n'
        for attr in sorted(dir(event)):
            if attr.startswith('_'): continue
            print attr.ljust(15), getattr(event, attr)

    def onMap(self, event):
        if isinstance(event.widget, tk.Toplevel):
            wdg = event.widget
            wdgName = getattr(wdg, 'windowname', None)
            self.mapped.append((wdg.winfo_name(), wdgName))
            print '\n<Map> ' + str(event.widget.__class__) + '\n'
            # self.printEvent(event)

    def onUnmap(self, event):
        if isinstance(event.widget, tk.Toplevel):
            ctrl = str(event.widget)
            self.mapped.pop()
            self.unmapped.append(ctrl)
            print '\n<Unmap> ' + str(event.widget.__class__) + '\n'
            self.printEvent(event)

def getActionFor(key, id=None, mod='', device='keyboard', windowsname=None):
    xmlfile = xbmc.translatePath('special://userdata/keymaps/%s.xml' % device)
    if not os.path.exists(xmlfile):
        xmlfile = xbmc.translatePath('special://xbmc/system/keymaps/%s.xml' % device)
    root = _parseXml(xmlfile)
    tags = []
    if windowsname: tags.append(windowsname)
    tags.append('global')

    if id is None:
        srchStr = './/%s' % key
    else:
        srchStr = './/%s[@id="%s"]' % (key, id)

    modset = set(mod.split(','))
    for tag in tags:
        etree = root.find('.%s/%s' % (tag, device))
        if etree is None: continue
        for selem in etree.findall(srchStr):
            if str(id) != selem.get('id', 'None'): continue
            emod = selem.get('mod', '')
            if set(emod.split(',')) == modset: break
        else:
            emod = None
        if emod is not None:
            actionStr = selem.text
            retval = ButtonTranslator.actions.get(actionStr.lower(), kodiKeyh.ACTION_NONE)
            break
    else:
        retval = kodiKeyh.ACTION_NONE
    return retval

def getActionStr(aval, prefix='ACTION_'):
    _action = dict( [('0x{:04x}'.format(ival), x) for x, ival in kodiKeyh.__dict__.items() if x.startswith(prefix)])
    actVal = '0x{:04x}'.format(aval)
    return _action.get(actVal, actVal)

mousemov=''
movcount=0
def onAction(note):
    global mousemov, movcount
    id = note.getId()
    actionName = getActionStr(id)
    if actionName == mousemov:
        movcount += 1
        if movcount % 10 == 0: print '.',
    if actionName != mousemov:
        if movcount > 0:
            print '.'
            print mousemov, movcount
            movcount = 0
        if actionName in ['ACTION_MOUSE_DRAG', 'ACTION_MOUSE_MOVE']:
            print actionName,
            mousemov = actionName
            movcount = 1
        else:
            mousemov = ''
            movcount = 0

    buttoncode = note.getButtonCode()
    if isinstance(buttoncode, basestring):
        keysym = buttoncode
        buttoncode = 0
    else:
        keysym = lookup(buttoncode, VK)[NAME]
    # keysym = chr(buttoncode) if buttoncode < 256 else 'NULL'
    amount1 = note.getAmount1()
    amount2 = note.getAmount2()
    if actionName in ['ACTION_MOUSE_DRAG', 'ACTION_MOUSE_MOVE']: return
    print 'actionName = ', actionName, 'actionValue = ', id, \
        'buttonCode = ', buttoncode, 'keysym = ', keysym, \
        'amount1 = ', amount1, 'amount2 = ', amount2

def mergeTexture():
    pass

def getTextSize(label, font, spacing=4):
    txt = Image.new('RGBA', (10, 10), (255, 255, 255, 0))
    d = ImageDraw.Draw(txt)
    return d.textsize(label, font, spacing=spacing)


def getLabel(label, font, textcolor, background=None, xpos=0, ypos=0, **options):
    SPACING = 4
    align = 'left'
    fnt = _eqTkFont(font)
    width = options.get('width', 0)
    if options.get('haspath', False) and width:
        lblwidth = fnt.getsize(label)[0]
        if lblwidth > width:
            newfile = os.path.basename(label)
            path = os.path.dirname(label)
            drive, path = os.path.splitdrive(path)
            while True:
                path, end = os.path.split(path)
                filename = newfile
                newfile = os.path.join(end, filename)
                newpath = os.path.join(drive, os.path.sep + '...', newfile)
                if fnt.getsize(newpath)[0] > width: break
            label = os.path.join(drive, os.path.sep + '...', filename)
        pass
    elif options.get('wrapmultiline', False) and width:
        lines = label.split('\n')
        label = ''
        for line in lines:
            words = line.split(' ')
            line = ''
            for word in words:
                lblwidth = fnt.getsize(line + ' ' + word)[0]
                if lblwidth > width:
                    label += line[1:] + '\n'
                    line = ' ' + word
                else:
                    line += ' ' + word
            label += line[1:] + '\n'
            pass
        label = label[:-1]

    txt = Image.new('RGBA', (width, 10), (255, 255, 255, 0))
    d = ImageDraw.Draw(txt)
    txtsize = d.textsize(str(label), fnt, spacing=SPACING)
    bshadow = options.get('shadowcolor', None)
    if bshadow: txtsize = (1 + txtsize[0], 1 + txtsize[1])

    txt = Image.new('RGBA', txtsize, (255, 255, 255, 0))
    d = ImageDraw.Draw(txt)
    if bshadow:
        shadowcolor = options['shadowcolor']
        colorTuple = _getThemeColour(shadowcolor)
        d.text((1, 1), label, font=fnt, fill=colorTuple, align=align, spacing=SPACING)
    colorTuple = _getThemeColour(textcolor)
    d.text((0, 0), str(label), font=fnt, fill=colorTuple, align=align, spacing=SPACING)
    if options.get('angle', 0):
        angle = options['angle']
        txt = txt.rotate(angle, expand=1)

    if not background: return txt
    Width, Height = background.size
    imgW, imgH = txtsize
    if options.get('alignment') == 'center':
        xpos += (Width - imgW)/2
    elif options.get('alignment') == 'right':
        xpos += (Width - imgW)
    if options.get('yalignment') == 'center':
        ypos += (Height - imgH)/2

    return background.paste(txt, box=(xpos, ypos), mask=txt)


def _eqTkFont(fontname, res='720p', fontset='Default'):
    pathName, skinDir = xbmc.translatePath('special://skin'), xbmc.getSkinDir()
    fontXml = os.path.join(pathName, skinDir, res, 'font.xml')
    fonts = xbmcaddon.Addon._parseXml(fontXml)
    fontset = fonts.find('.//fontset[@id="%s"]' % fontset)
    font = fontset.find('.//font[name="%s"]' % fontname)
    if font is None: font = fontset.find('.//font[name="font13"]')
    if font is not None:
        keys = ['filename', 'size', 'style']
        attrib = dict((chld.tag, chld.text) for chld in font.getchildren() if chld.tag in keys)
        filename = attrib['filename']
        size = int(attrib['size'])
        if attrib.has_key('style'):
            # Here we must find a way to detect the correct filename
            pass
    else:
        filename = 'arial.ttf'
        size = 20
    path = xbmc.translatePath('special://xbmc/')
    fullname1 = os.path.join(path, 'addons', skinDir, 'fonts', filename)
    fullname2 = os.path.join(path, 'media', 'fonts', filename)
    for fullname in [fullname1, fullname2]:
        if os.path.exists(fullname):
            filename = fullname
            break
    return ImageFont.truetype(filename, size)

def _imageFile(imageFile):
    if not os.path.dirname(imageFile):
        imageFile = os.path.join(TEXTURE_DIRECTORY, imageFile)
    if not os.path.exists(imageFile): return None
    return imageFile

@memoize
def getTexture(imageFile, Width, Height, aspectratio='stretch', **options):
    imageFile = _imageFile(imageFile)
    if not imageFile: return None
    im = Image.open(imageFile)
    bbox = im.getbbox()
    im = im.crop(bbox)
    iw, ih = im.size

    if options.get('flipx', False):
        im = im.transpose(Image.FLIP_LEFT_RIGHT)

    if options.get('flipy', False):
        im = im.transpose(Image.FLIP_TOP_BOTTOM)

    if options.get('colorkey'):
        colorkey = options.get('colorkey')
        colorTuple = _getThemeColour(colorkey)
        base = Image.new('RGBA', (iw, ih), colorTuple)
        im = Image.alpha_composite(base, im)
    if aspectratio == 'stretch':
        width, height = Width, Height
    elif aspectratio == 'keep':
        width, height = min(Width, int((1.0*iw*Height)/ih)), min(Height, int((1.0*ih*Width)/iw))
    elif aspectratio == 'scale':
        width, height = max(Width, int((1.0*iw*Height)/ih)), max(Height, int((1.0*ih*Width)/iw))
    elif aspectratio == 'center':
        width, height = iw, ih

    dstIm = Image.new(im.mode, (width, height), (128, 128, 128, 128))

    brdSectors = lambda w, h: [(    0,     0,     l,     t),
                               (    l,     0, w - r,     t),
                               (w - r,     0,     w,     t),
                               (    0,     t,     l, h - b),
                               (w - r,     t,     w, h - b),
                               (    0, h - b,     l,     h),
                               (    l, h - b, w - r,     h),
                               (w - r, h - b,     w,     h)]
    coreRegion = lambda w, h:  (    l,     t, w - r, h - b)

    border = options.get('border', 0)
    if isinstance(border, basestring):
        border = map(int, border.split(','))
    else:
        border = (border, )
    border *= 4
    l, t, r, b = border[:4]

    coreSrc = coreRegion(iw, ih)
    coreRgn = im.crop(coreSrc)

    if options.get('bordertexture', '') and options.get('bordersize', None):
        bordertexture = options["bordertexture"]
        im = Image.open(bordertexture)
        iw, ih = im.size

        bordersize = options['bordersize']
        if isinstance(bordersize, int):
            bordersize = (bordersize, )
        bordersize *= 4
        l, t, r, b = bordersize[:4]

    srcSectors = brdSectors(iw, ih)
    dstSectors = brdSectors(width, height)
    for srcBox, dstBox in  zip(srcSectors, dstSectors):
        dstSize = (dstBox[2] - dstBox[0], dstBox[3] - dstBox[1])
        if dstSize[0] <= 0 or dstSize[1] <= 0: continue
        region = im.crop(srcBox)
        region = region.resize(dstSize)
        dstIm.paste(region, dstBox)

    coreDst = coreRegion(width, height)
    dstSize = (coreDst[2] - coreDst[0], coreDst[3] - coreDst[1])
    if dstSize[0] > 0 and dstSize[1] > 0:
        coreReg = coreRgn.resize(dstSize)
        dstIm.paste(coreReg, coreDst)

    colordiffuse = options.get('colordiffuse', None)
    if colordiffuse:
        colorTuple = _getThemeColour(colordiffuse)
        colordiffuse = Image.new(im.mode, (width, height), colorTuple)

    diffuse = options.get('diffuse', None) or colordiffuse
    if diffuse:
        dstIm = ImageChops.multiply(dstIm, diffuse)

    xOff, yOff = (Width - width)/2, (Height - height)/2
    if aspectratio == 'scale': xOff = yOff = 0
    if xOff >= 0:
        x1s, x2s = 0, min(Width, width)
        x1d, x2d = xOff + x1s, xOff + x2s
    else:
        xOff = -xOff
        x1d, x2d = 0, Width
        x1s, x2s = xOff + x1d, xOff + x2d

    if yOff >= 0:
        y1s, y2s = 0, min(Height, height)
        y1d, y2d = yOff + y1s, yOff + y2s
    else:
        yOff = -yOff
        y1d, y2d = 0, Height
        y1s, y2s = yOff + y1d, yOff + y2d


    retIm = Image.new(im.mode, (Width, Height), (128, 128, 128, 128))
    region = dstIm.crop((x1s, y1s, x2s, y2s))
    retIm.paste(region, (x1d, y1d, x2d, y2d))
    return retIm


def _getThemeColour(srchcolor, theme='Confluence'):
    if not re.match('[0-9ABCDEF]{8}\Z', srchcolor.upper()):
        pathName, skinDir = xbmc.translatePath('special://skin'), xbmc.getSkinDir()
        colorXml = theme + '.xml'
        files = ['defaults.xml', colorXml]
        color = None
        while files:
            filename = files.pop()
            filename = os.path.join(pathName, skinDir, 'Colors', filename)
            if not os.path.exists(filename): continue
            colors = _parseXml(filename)
            color = colors.find('.//color[@name="%s"]' % srchcolor)
            if color is not None: break

        if color is None:
            try:
                colorTuple = ImageColor.getrgb(srchcolor)
            except ValueError:
                color = colors.find('.//color[@name="invalid"]')
            else:
                if len(colorTuple) == 3: colorTuple += (255, )
                return colorTuple

        srchcolor = color.text if color is not None else 'FFFF0000'
    color = [int(srchcolor[k:k+2], 16) for k in range(0, 8, 2)]
    transp, red, green, blue = color
    return (red, green, blue, transp)

def getImageBBox(imgLayout, listItem, fontTbl=None):
    fontTbl = fontTbl or {}
    x1 = y1 = x2 = y2 = 0
    Width, Height = listItem.getProperty('width'), listItem.getProperty('height')
    for item in imgLayout:
        getPosAndDim(item, Width, Height)
        x = item['left']
        y = item['top']
        itype = item['type']
        if itype == 'image':
            width = item['width']
            height = item['height']
        elif itype == 'label':
            fntName = item['font']
            font = fontTbl.get(fntName, None)
            if not font:
                font = _eqTkFont(fntName)
                fontTbl[fntName] = font
            label = item['label']
            if label: txtW, txtH = getTextSize(str(label), font)
            else: txtW, txtH = 0, 0

            x += item.get('xoffset', 0)
            y += item.get('yoffset', 0)
            width = max(item.get('width',0), txtW)
            height = max(item.get('height',0), txtH)
        else:
            raise Exception('Type %s is not allowed' % itype)
        x1, x2 = min(x1, x), max(x2, x + width)
        y1, y2 = min(y1, y), max(y2, y + height)

    return(x1, y1, x2, y2)

def getPosAndDim(posIn, scrResW, scrResH):
    width = posIn.get('width', scrResW)
    height = posIn.get('height', scrResH)

    int_set = set(posIn.keys()).intersection(['posx', 'left', 'right', 'centerleft', 'centerright'])
    if not int_set:
        x = 0
    else:
        key = int_set.pop()
        value = posIn.pop(key)
        if key in ['left', 'posx']:
            if isinstance(value, int):
                x = value
                if not posIn.has_key('width'): width = width - x
            else: x = scrResW - int(value[:-1])
        elif key == 'right':
            if isinstance(value, basestring): raise Exception('"r" suffix not allowed in right tag')
            x = scrResW - value - width
        elif key == 'centerleft':
            x = value - width/2
        elif key == 'centerright':
            x = scrResW - value - width / 2

    int_set = set(posIn.keys()).intersection(['posy', 'top', 'bottom', 'centertop', 'centerbottom'])
    if not int_set:
        y = 0
    else:
        key = int_set.pop()
        value = posIn.pop(key)
        if key in ['top', 'posy']:
            if isinstance(value, int):
                y = value
                if not posIn.has_key('height'): height = height - y
            else: y = scrResH - int(value[:-1])
        elif key == 'bottom':
            if isinstance(value, basestring): raise Exception('"r" suffix not allowed in bottom tag')
            y = scrResH - value - height
        elif key == 'centertop':
            y = value - height/2
        elif key == 'centerbottom':
            y = scrResH - value - height/2

    posIn.update(dict(left=x, top=y, width=width, height=height))



def getImageFromLayout(imgLayout, listItem, cache=False):
    global imgCache
    if not listItem: raise Exception('No listItem supplied')
    if cache:
        triggers = listItem.getTriggers()
        try:
            texture = triggers.pop('texture')
        except:
            cache = False
        else:
            texture = listItem.getProperty(texture)
            triggers = [(key, listItem.getProperty(key)) for key in sorted(triggers)]
            key = texture + str(imgLayout)
            if key in imgCache:
                triggersAttr, baseImg = imgCache[key]
                if triggers == triggersAttr: return baseImg

    lytStr = json.dumps(imgLayout)
    lytStr = re.sub(r'item\.(\w+)',lambda x: str(listItem.getProperty(x.group(1)) if listItem.getProperty(x.group(1)) is not None else 'null'), lytStr)
    lytStr = re.sub(r'"([0-9]+|null)"',lambda x: x.group(1), lytStr)
    lytStr = lytStr.replace('\n', '\\n')
    imgLayout = json.loads(lytStr, strict=False)
    x0, y0, x2, y2 = getImageBBox(imgLayout, listItem)
    baseImg = Image.new('RGBA', (x2 - x0, y2 - y0), (0, 0, 0, 0))
    for alayout in imgLayout:
        item = alayout.copy()
        itype = item.pop('type')
        xpos, ypos, width, height = map(item.pop, ('left', 'top', 'width', 'height'))
        if itype == 'image':
            if isinstance(item['texture'], dict):
                txtAttr = item.pop('texture')
                item['texture'] = txtAttr.pop('value')
                item.update(txtAttr)
            texture = None
            imgFile = item.pop('texture')
            if imgFile and _imageFile(imgFile):
                texture = getTexture(imgFile, width, height, **item)
                baseImg.paste(texture, box=(xpos - x0, ypos - y0))
        elif itype == 'label':
            label = item.pop('label')
            if label is not None:
                trnfDict = dict(align='alignment', aligny='yalignment', textcolor='color')
                toTranslate = set(trnfDict.keys()).intersection(item.keys())
                while toTranslate:
                    oldkey = toTranslate.pop()
                    newkey = trnfDict[oldkey]
                    item[newkey] = item.pop(oldkey)

                font = item.pop('font')
                textcolor = item.pop('color', 'white')
                x1 = item.get('textoffsetx', 0) if item.get('alignment') == 'left' else 0
                y1 = item.get('textoffsety', 0) if item.get('yalignment') == 'top' else 0
                getLabel(label, font, textcolor, background=baseImg, xpos=x1, ypos=y1, **item)

                # imgW, imgH = txtImg.size
                #
                # if item.get('alignment') == 'center':
                #     x1 += (width - imgW)/2
                # elif item.get('alignment') == 'right':
                #     x1 += (width - imgW)
                # if item.get('yalignment') == 'center':
                #     y1 += (height - imgH)/2
                #
                # baseImg.paste(txtImg, box=(x1, y1))

    if cache:
        imgCache[key] = (triggers, baseImg)
    return baseImg

if __name__ == '__main__':
    # fileName = r'C:\testFiles\Confluence\dialogback2.png'
    # root = tk.Tk()
    # img = Image.open(fileName)
    # alpha = img.convert(mode='1')
    # img.putalpha(alpha)
    # img = ImageTk.PhotoImage(img)
    # tk.Label(root, image=img, bg='black').pack()
    # root.mainloop()


    # bdtexture = r'C:\testFiles\Confluence\\button-focus.png'
    # fileName = r'C:\Users\Alex Montes Barrios\AppData\Roaming\Kodi\addons\plugin.video.xbmcmodule\resources\skins\Default\media\marco.png'
    #
    # root = tk.Tk()
    # imgPhoto = getTexture(fileName, 610, 240, border=120, colordiffuse="FFAAAAAA", flipx=True, flipy=True)
    # imgPhoto = getTexture(fileName, 64, 32)
    # color = _getThemeColour('grey5')
    # imgPhoto = getTexture(fileName, 550, 350, bordersize=5, bordertexture=bdtexture, aspectratio='center')
    # packparam = dict(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
    # imgPhoto = []
    # imgPhoto.append(getLabel('Label sin sombra', 'WeatherTemp', 'white'))
    # imgPhoto.append(getLabel('Label con sombra', 'WeatherTemp', 'white', shadowcolor='yellow'))
    # imgPhoto.append(getLabel('Label angle=45', 'WeatherTemp', 'white', angle=45))
    # imgPhoto.append(getLabel('linea1\nlinea2\nlinea3', 'WeatherTemp', 'white'))
    # imgPhoto.append(getLabel('linea con wrapmultiline true y width = 500 pero con esto es\nun salto de linea', 'WeatherTemp', 'white', wrapmultiline=True, width=500))
    # imgPhoto.append(getLabel('c:/este/recorrer/es/un/camino/largo/por/fin.txt', 'WeatherTemp', 'white', haspath=True, width=800))
    # for img in imgPhoto:
    #     tk.Label(root, image=img, bg='black').pack(packparam)
    # root.mainloop()




    # actionid = getActionFor('p', mod='ctrl', windowsname='LoginScreen')
    # actionid = getActionFor('wheelup', device='mouse', windowsname='LoginScreen')
    # actionid = getActionFor('wheelup', device='mouse', windowsname='SlideShow')
    # actionid = getActionFor('key', id=65446, windowsname='LoginScreen')
    # actionid = getActionFor('p', windowsname='LoginScreen')




    # def prnt(event, msg):
    #     print msg
    #
    # root = tk.Tk()
    # root.bind_all('<Button-1>', lambda x,y='bindall:Button-1':prnt(x,y))
    # root.title('ROOT')
    # root.withdraw()
    # top = tk.Toplevel(root)
    # top.title('top')
    # top.attributes('-fullscreen', True)
    # top.bind('<Button>', lambda x, y='bindtop:Button': prnt(x, y))
    # frm2 = tk.Label(top, bg='red')
    # frm2.bind_class('Frame', '<Button-2>', lambda x, y='bindclass:Button-2': prnt(x, y))
    # frm2.place(x=500, y=200,width=200, height=200)
    # frm1 = tk.Frame(top, bg='black')
    # frm1.bind('<Button-1>', lambda x, y='bindinstance:Button-1': prnt(x, y))
    # frm1.place(x=200, y=200, width=200, height=200 )
    # root.mainloop()

    # def prnt1(event):
    #     print 'Button:topLev'
    #     return True
    # def prnt2(event):
    #     print 'Motion:topLev'
    #     return False
    # def prnt3(event):
    #     print 'numpad:topLev'
    #
    # root = AppWindow()
    # root.withdraw()
    # topLev = tk.Toplevel(root)
    # setattr(topLev, 'onAction', onAction)
    # # topLev.bind('<Button>', prnt1)
    # # topLev.bind('<Motion>', prnt2)
    # # topLev.event_add('<<instnumpad>>', '<Up>', '<Down>','<Left>', '<Right>', '<Prior>', '<Next>')
    # # topLev.bind('<<instnumpad>>', prnt3)
    # # topLev.attributes("-alpha", 0.01)
    # # topLev.state("zoomed")
    # # topLev.overrideredirect(True)
    # canvas = tk.Canvas(topLev, bg='black', height=400, width=400, borderwidth=0)
    # canvas.place(relwidth=1.0, relheight=1.0)
    # # bgimg = Image.new('RGBA', (400, 400), (255, 255, 255, 128))
    # bgimg = ImageGrab.grab()
    # photo = ImageTk.PhotoImage(bgimg)
    # canvas.create_image(0, 0, image=photo, anchor='nw')
    #
    # frm2 = tk.Label(topLev, bg='red')
    # # frm2.bind_class('Frame', '<Button-2>', lambda x, y='bindclass:Button-2': prnt(x, y))
    # frm2.place(x=500, y=200,width=200, height=200)
    # frm1 = tk.Frame(topLev, bg='black')
    # # frm1.bind('<Button-1>', lambda x, y='bindinstance:Button-1': prnt(x, y))
    # frm1.place(x=200, y=200, width=200, height=200 )
    #
    # # topLev.focus_set()
    # # label = tk.Button(topLev,takefocus=1, text='Esto es un label', font=('Roman', 20, 'bold'), fg='red')
    # # label.place(x=400, y=300)
    # # label.focus_set()
    # root.mainloop()



    # getControlsFromFile('DialogDownloadProgress.xml',
    #                     scriptPath=r'C:\Users\Alex Montes Barrios\AppData\Roaming\Kodi\addons\script.module.simple.downloader\resources\skins',
    #                     defaultSkin="Default",
    #                     defaultRes='720p')

    # getControlsFromFile('testCase.xml', scriptPath='c:/testFiles',defaultSkin='', defaultRes='')
    # getControlsFromFile('home.xml', scriptPath='')
    # filename = r'C:\Program Files\Kodi\addons\skin.confluence\720p\DialogKeyboard.xml'
    # filename = r'C:\Program Files\Kodi\addons\skin.confluence\720p\DialogOK.xml'
    # window, controls = getRoots('DialogKeyboard.xml', scriptPath='')
    # # window = processRoot(window)
    # ctrList = processRoot(controls)
    # normControlMap(ctrList, 1280, 720)
    # pass

    # root = tk.Tk()
    # canvas = tk.Canvas(root, width=300, height=600, bg='green')
    # canvas.pack(fill=tk.BOTH, expand=tk.YES)
    # cnvChild1 = tk.Canvas(canvas, width=300, height=300)
    # cnvChild2 = tk.Canvas(canvas, width=300, height=300)
    #
    # img1 = getTexture(r'C:\testFiles\Confluence\button-nofocus.png', 300, 300, border=10)
    # img1 = ImageTk.PhotoImage(img1)
    #
    # img2 = getTexture(r'C:\testFiles\Confluence\defaultaddonalbuminfo.png', 300, 300)
    # img2 = ImageTk.PhotoImage(img2)
    #
    # wndId2 = canvas.create_window(0, 200, window=cnvChild2, anchor=tk.NW)
    # cnvChild2.create_image(0, 0, image=img2, anchor=tk.NW)
    # wndId1 = canvas.create_window(0, 0, window=cnvChild1, anchor=tk.NW)
    # cnvChild1.create_image(0,   0, image=img1, anchor=tk.NW)
    #
    # canvas.lift(wndId1, wndId2)
    # root.mainloop()
    # # for k in [4]:
    # #     ctrMap = ctrList[k].copy()
    # #     print mapControl(ctrMap, 1280, 720)
    # #
    # #
    # # # from xbmcgui import ListItem
    # # # root = tk.Tk()
    # # #
    # # # itemLayout = [
    # # #             {u'colorkey': None,
    # # #              u'aspectratio': 'stretch',
    # # #              u'height': 100,
    # # #              u'left': 0,
    # # #              u'texture': {u'border': 0, u'value': 'item.texture'},
    # # #              u'top': 0,
    # # #              u'type': u'image',
    # # #              u'width': 100,
    # # #              u'colordiffuse': 'item.colordiffuse'}]
    # # #
    # # # params =  dict(colorkey=0, aspectratio='stretch', height=430, width=860)
    # # # itemprop = dict(texture='DialogBack2.png')
    # # #
    # # # itemLayout[0].update(params)
    # # #
    # # # litem = ListItem()
    # # # for key, value in itemprop.items():
    # # #     litem.setProperty(key, value)
    # # # itemImg1 = getImageFromLayout(itemLayout, litem)
    # #
    # #
    # #
    # #
    # # #
    # # # itemLayout = [
    # # #                 {u'ID': u'1',
    # # #                  u'MASTERID': u'0',
    # # #                  u'colorkey': 0,
    # # #                  u'description': u'background image',
    # # #                  u'elem_tag': u'control',
    # # #                  u'height': 430,
    # # #                  u'left': 0,
    # # #                  u'texture': {u'border': 40, u'value': u'DialogBack2.png'},
    # # #                  u'top': 0,
    # # #                  u'type': u'image',
    # # #                  u'width': 860},
    # # #                 {u'ID': u'2',
    # # #                  u'MASTERID': u'0',
    # # #                  u'colorkey': 0,
    # # #                  u'description': u'Dialog Header image',
    # # #                  u'elem_tag': u'control',
    # # #                  u'height': 40,
    # # #                  u'left': 40,
    # # #                  u'texture': u'dialogheader.png',
    # # #                  u'top': 16,
    # # #                  u'type': u'image',
    # # #                  u'width': 780},
    # # #                 {u'ID': u'3',
    # # #                  u'MASTERID': u'0',
    # # #                  u'align': u'center',
    # # #                  u'aligny': u'center',
    # # #                  u'description': u'header label',
    # # #                  u'disabledcolor': u'grey3',
    # # #                  u'elem_tag': u'control',
    # # #                  u'font': u'font13_title',
    # # #                  u'height': 30,
    # # #                  u'id': 311,
    # # #                  u'label': u'Este label es agregado',
    # # #                  u'left': 40,
    # # #                  u'shadowcolor': u'black',
    # # #                  u'textcolor': u'selected',
    # # #                  u'top': 20,
    # # #                  u'type': u'label',
    # # #                  u'width': 780}]
    # # # # itemLayout = [ dict(type='image', left=0, top=0, width=400, height=42,
    # # # #                     border=5, texture='floor_buttonFO.png'),
    # # # #                dict(type='image', left=5, top=5, width=32, height=32,
    # # # #                     border=0, texture='icon_back.png'),
    # # # #                dict(type='label', label='Item21', left=50, top=0, width=350, height=42,
    # # # #                     xoffset=7, yoffset=0, font='font13', textcolor='red',
    # # # #                     yalignment='center', alignment='left')
    # # # #                ]
    # # # itemImg1 = ImageTk.PhotoImage(itemImg1)
    # # # tk.Label(root, image=itemImg1).pack()
    # # # # # itemLayout = [ dict(type='image', left=0, top=0, width=400, height=42,
    # # # # #                     border=(5, 5, 5, 5), texture='keyboardkeynf.png'),
    # # # # #                dict(type='label', label='A', left=0, top=0, width=400, height=42,
    # # # # #                     xoffset=0, yoffset=0, font='font13', textcolor='red',
    # # # # #                     yalignment='center', alignment='center')
    # # # # #                ]
    # # # # # itemImg2 = ImageTk.PhotoImage(getImageFromLayout(itemLayout))
    # # # # # tk.Label(root, image=itemImg2).pack()
    # # # root.mainloop()
    # #
    # # # pass
    # # #
    # # # print set([elem['type'] for elem in ctrList])
    # # # controls = []
    # # #
    # # # root = tk.Tk()
    # # #
    # # # for k in range(len(ctrList)):
    # # # # for k in [4]:
    # # #     answ = mapArgsKwargs(ctrList, k)
    # # #     genTags, args, kwargs, navTags = answ
    # # #     ctrClassName = genTags['ctrClass']
    # # #     ctrClass = getattr(tkintertest, ctrClassName)
    # # #     control = ctrClass(*args, **kwargs)
    # # #     px, py = control.getPosition()
    # # #     control.place(x=px, y=py)
    # # #     controls.append(control)
    # # #
    # # # root.mainloop()
    pass