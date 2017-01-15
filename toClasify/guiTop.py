import Tkinter as tk
import inspect
import os
import re
import xml.etree.ElementTree as ET

from fromC import ButtonTranslator
from fromC.Keytable import VK, NAME, lookup

from KodiAddonIDE.KodiStubs.fromC import key as kodiKeyh
from KodiAddonIDE.KodiStubs.xbmcModules import xbmc


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
    def __eq__(self, other):
        return self.getId() == other

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

    def mapWindow(self, window):
        self.mapped.append(window)

    def getWindowFromId(self, windowId):
        if windowId != -1:
            for window in self.mapped:
                if window.windowId == windowId:
                    return window
        return None

    def toNotify(self, ctrl, action, id, mod='', event=None, device='mouse'):
        window = self.mapped[-1]
        # wndId = window.windowId
        # wdgname = [key for key,value in ButtonTranslator.windows.items() if value == wndId]
        # wdgname = wdgname[0] if wdgname else ''
        wdgname = window.wndfile
        if device:
            actionId = getActionFor(action, id, mod, device, windowsname=wdgname)
            if wdgname:
                if ctrl and ctrl.getId() and actionId in [ButtonTranslator.ACTION_MOUSE_LEFT_CLICK, ButtonTranslator.ACTION_SELECT_ITEM]:
                    window.onClick(ctrl)
            else:
                if ctrl and actionId in [ButtonTranslator.ACTION_MOUSE_LEFT_CLICK, ButtonTranslator.ACTION_SELECT_ITEM]:
                    window.onControl(ctrl)
            actionInst = AppAction(actionId, action, 1.0*event.x_root, amnt2=1.0*event.y)
            window.onAction(actionInst)
        else:
            if wdgname:
                ctrlId = ctrl.getId() or 0
                window.onFocus(ctrlId)

    def _wndattr(self):
        wdgid, wdgname = self.mapped[-1]
        wdg = self.nametowidget(wdgid)
        return wdg, wdgname


    def onInit(self):
        self.mapped = []
        self.unmapped  = []

    def onMouseClick(self, event):
        pass

    def onMouseMove(self, event):
        pass

    def onKey(self, event):
        pass

    def onMouse(self, event):
        pass

    def notifyEvent(self, message):
        print message


class WindowBase(object):

    """ControlGroup class."""

    def __init__(self):
        """
        x: integer - x coordinate of control.
        y: integer - y coordinate of control.
        width: integer - width of control.
        height: integer - height of control.

        Example:
        self.group = xbmcgui.ControlGroup(100, 250, 125, 75)
        """
        super(WindowBase, self).__init__()

        self.master = None
        self._xorig = 0
        self._yorig = 0

        self.widget = None
        self.focus = None

        self._mouseX = 0
        self._mouseY = 0
        self._mouseT = 0
        self._mouseState = ''
        self.mouseStop = None
        pass

    def _setWidgetBinds(self):
        ctrlWdg = self.focus.widget
        ctrlWdg.bind('<Key>', self._onKey)

        ctrlWdg.event_add('<<navigation>>', '<Up>', '<Down>', '<Left>', '<Right>', '<Home>', '<End>', '<Prior>', '<Next>')
        ctrlWdg.bind('<<navigation>>', self._onNavigation)

        ctrlWdg.event_add('<<mouseaction>>', '<Button>', '<ButtonRelease>', '<Motion>', '<MouseWheel>')
        ctrlWdg.bind('<<mouseaction>>', self._onMouse)


    def _createContainer(self, parent, control):
        w, h = control.getWidth(), control.getHeight()
        control.widget = ctrlWdg = tk.Canvas(parent, width=w, height=h, highlightthickness=0, bd=0, bg='black', takefocus=1, scrollregion=(0, 0, 10*w, 10*h))
        control._setWidgetBinds()
        return ctrlWdg

    def _isContainer(self, control):
        return control.ctrlType == 'container'

    def _isWindow(self, control):
        return control.ctrlType == 'compound'

    def _registerControl(self, control):
        if hasattr(control, '_wdgID'): raise ReferenceError('The control has been mapped to another window previously')
        control.master = master = control.master or self.focus
        wdg = master.widget
        xpos, ypos = control.getPosition()
        xpos += master._xorig
        ypos += master._yorig
        if self._isContainer(control):
            control.widget = wdg
            control._wdgID = wdgID = wdg.create_image(xpos, ypos, anchor=tk.NW)
            control._xorig, control._yorig = xpos, ypos
        elif self._isWindow(control):
            ctrlWdg = self._createContainer(wdg, control)
            control._wdgID = wdgID = wdg.create_window(xpos, ypos, window=ctrlWdg, anchor=tk.NW, tags='container')
        else:
            def onEnter(event, ctrl=control):
                return self._onEnter(event, ctrl)
            def onLeave(event, ctrl=control):
                return self._onLeave(event, ctrl)
            control._wdgID = wdgID = wdg.create_image(xpos, ypos)
            control._setWdgImage()
            wdg.itemconfigure(wdgID, image=control.wdgImg, anchor=tk.NW)
            wdg.tag_bind(wdgID, '<Enter>', onEnter)
            wdg.tag_bind(wdgID, '<Leave>', onLeave)
        control._wdgIdPath =  str(master._wdgID) + '.' + str(control._wdgID)
        tag1 = re.findall('\.([^ ]+) ', str(control))[0]
        tag2 = 'grp' + str(master._wdgID).rjust(3, '0')
        wdg.itemconfigure(wdgID, tags=(tag1, tag2))

        control.master = master

    def _onMouse(self, event):
        key = ''
        id = None
        if event.num in [4,5]:
            key = 'wheelup' if event.num == 4 else 'wheeldown'
        if event.type == '4': # BUTTON
            deltaT = abs(event.time - self._mouseT)
            if deltaT < 200:
                key = 'doubleclick'
                id = event.num - 1
                self._mouseState = key
            self._mouseX = event.x_root
            self._mouseY = event.y_root
            self._mouseT = event.time
        elif event.type == '5': # BUTTONRELEASE
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
        elif event.type == '6': # MOTION
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
        elif event.type == '38': # MOUSEWHEEL
            key = 'wheelup' if event.delta > 0 else 'wheeldown'
        if not key: return
        focusWdg = self._getFocusedWidget()
        if not focusWdg or not focusWdg._isSelected:
            focusWdg = 0
        elif not hasattr(focusWdg, 'widget'):
            if key == 'leftclick':
                self._onAction(focusWdg, '_onClick', event)
            if key == 'mousemove':
                self._onAction(focusWdg, '_onMotion', event)
            if key == 'mousedrag':
                self._onAction(focusWdg, '_onDrag', event)

        root = AppWindow()
        root.toNotify(focusWdg, key, id, event=event, device='mouse')

    def _onKey(self, event):
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
        keymod = {'ctrl':0x0004,'shift':0x0001|0x0002,'alt':0x0080}
        mod = []
        for key in keymod:
            if event.state & keymod[key]:
                mod.append(key)
        mod = ','.join(mod)
        focusWdg = self._getFocusedWidget()
        if not focusWdg or not focusWdg._isSelected: return
        if not hasattr(focusWdg, 'widget'):
            if keysym == 'return':
                self._onAction(focusWdg, '_onClick', None)
            else:
                self._onAction(focusWdg, '_onKey', event)
        root = AppWindow()
        root.toNotify(focusWdg, keysym, id, mod, event, device='keyboard')

    def _getFocusedWidget(self):
        focusWdg = self.focus
        while self._isContainer(focusWdg) and focusWdg._isSelected:
            focusWdg = focusWdg.focus
        return focusWdg

    def _onNavigation(self, event):
        focusWdg = self._getFocusedWidget()
        if not focusWdg or not focusWdg._isSelected: return
        if not hasattr(focusWdg, 'widget'):
            self._onAction(focusWdg, '_onKey', event)
        selfgrp = focusWdg.master
        self.mouseStop = self.mouseStop or focusWdg
        if self.mouseStop == focusWdg: self.mouseMoveFlag = True
        nav = event.keysym
        if nav not in ['Up', 'Down', 'Left', 'Right']: return
        control = focusWdg.navMap.get(nav, None)
        if control:
            ctrlgrp = control.master
        elif selfgrp.navMap.get(nav, None):
            control = selfgrp.navMap[nav]
            ctrlgrp = selfgrp.master
        if control:
            if selfgrp._isContainer(control):
                selfgrp.focus = control
                selfgrp.checkScroll(ctrlgrp, control)
                ctrlgrp = control
                control = control.focus
            if ctrlgrp != selfgrp:
                ctrlgrp.mouseStop = selfgrp.mouseStop
                selfgrp.mouseStop = None
            selfgrp._onLeave(None, focusWdg)
            ctrlgrp._onEnter(None, control)
            selfgrp.checkScroll(ctrlgrp, control)


    def checkScroll(self, ctrlgrp, control, vwcoords=None):
        canvas = ctrlgrp.widget
        w, h = control.getWidth(), control.getHeight()
        xpos, ypos = control.getPosition()
        wdgcoords = (xpos, ypos) + (xpos + w, ypos + h)
        if not vwcoords:
            width, height = canvas.winfo_width(), canvas.winfo_height()
            vwcoords = (canvas.canvasx(0), canvas.canvasy(0)) + (canvas.canvasx(width), canvas.canvasy(height))
        deltax = min(wdgcoords[0], vwcoords[0]) - vwcoords[0] + max(wdgcoords[2], vwcoords[2]) - vwcoords[2]
        deltay = min(wdgcoords[1], vwcoords[1]) - vwcoords[1] + max(wdgcoords[3], vwcoords[3]) - vwcoords[3]
        if deltax != 0 or deltay != 0:
            dx, dy = int(deltax), int(deltay)
            p1 = (max(0, dx), max(0, dy))
            p2 = (-min(0, dx), -min(0, dy))
            canvas.scan_mark(*p1)
            canvas.scan_dragto(*p2, gain=1)
            pass

    def _onEnter(self, event, control):
        if self._mouseState == 'mousedrag':return
        master = control.master
        wdg = master.widget
        wdg.focus_set()
        master._setFocusOn(control)
        root = AppWindow()
        root.toNotify(control, 'onEnter', id=0, event=None, device='')


    def _onLeave(self, event, ctrl):
        if self._mouseState == 'mousedrag':return
        if not self._isContainer(ctrl): ctrl.updateCanvas(False)

    def _onAction(self, ctrl, action, *args):
        if not hasattr(ctrl, action): return
        actionMethod = getattr(ctrl, action)
        if args:
            actionMethod(*args)
        else:
            actionMethod()

class ListItemWrapper:
    def __init__(self, listItemObj, triggers=None, funcToTrigger=None):
        self.setTriggers(triggers or {})
        self._cbTrigger = funcToTrigger
        self.wrapfunc(listItemObj, 'setProperty')
        self._obj = listItemObj

    def getTriggers(self):
        return self._triggers

    def setTriggers(self, triggers):
        if triggers:
            self._triggers = set(['width', 'height']).union(triggers)
        else:
            self._triggers = None

    def __getattr__(self, item):
        return getattr(self._obj, item)

    def default_tracing_processor(self, original_callable, obj, *args, **kwargs):
        r_name = getattr(original_callable, '__name__', '<unknown>')
        if args: kwargs = {args[0]:args[1]}
        try:
            for key, value in kwargs.items():
                result = original_callable(obj, key, value)
        except:
            raise
        else:
            triggers = self.getTriggers()
            if triggers:
                int_set = triggers.intersection(kwargs.keys())
                if int_set and self._cbTrigger:
                    self._cbTrigger()
            return result

    def wrapfunc(self, obj, name, processor=None, avoid_doublewrap=True):
        if not processor:
            processor = self.default_tracing_processor
        call = getattr(obj, name)
        if avoid_doublewrap and getattr(call, 'processor', None) is processor:
            return

        original_callable = getattr(call, 'im_func', call)

        def wrappedfunc(*args, **kwargs):
            return processor(original_callable, obj, *args, **kwargs)

        wrappedfunc.original = call
        wrappedfunc.processor = processor
        if inspect.isclass(obj):
            if hasattr(call, 'im_self'):
                if call.im_self:
                    wrappedfunc = classmethod(wrappedfunc)
            else:
                wrappedfunc = staticmethod(wrappedfunc)
        setattr(obj, name, wrappedfunc)

    def unwrapfunc(self, obj, name):
        setattr(obj, name, getattr(obj, name).original)

